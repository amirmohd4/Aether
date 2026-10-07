from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from .api_models import HumanDecisionRequest, StartCaseRequest
from .engine import engine
from .requirements_engine import RequirementEngine
from .rule_registry import RuleRegistry
from .verification import VerificationEngine
from .security import Principal, require_principal, require_role
from .understanding import ObjectiveUnderstandingEngine

router = APIRouter(prefix="/api/aether/v2", tags=["Aether V2"], dependencies=[Depends(require_principal)])
requirements_engine = RequirementEngine()
understanding_engine = ObjectiveUnderstandingEngine()
rule_registry = RuleRegistry()
verification_engine = VerificationEngine()


def serialize(case):
    return {
        "summary": case.summary(),
        "requirements": case.requirements,
        "tasks": {
            task_id: {
                "name": state.definition.name,
                "department": state.definition.department,
                "worker": state.definition.worker,
                "dependencies": state.definition.dependencies,
                "status": state.status.value,
                "authority_required": state.definition.authority_required,
                "physical_action": state.definition.physical_action,
                "result": state.result,
                "error": state.error,
                "evidence": state.evidence,
                "attempts": state.attempts,
                "idempotency_key": state.idempotency_key,
            }
            for task_id, state in case.tasks.items()
        },
        "human_actions": case.human_actions,
        "exceptions": case.exceptions,
        "evidence": case.evidence,
        "outcome": case.outcome,
        "verification": verification_engine.reconcile({
            task_id: task.result
            for task_id, task in case.tasks.items()
            if task.result
        }).as_dict(),
        "queue": engine.queue.for_case(case.case_id),
        "execution_events": case.execution_events[-50:],
    }


@router.get("/connectors")
def connector_catalog():
    return {
        "connectors": engine.workers.connector_catalog(),
        "default_mode": "synthetic",
        "production_connectors_configured": False,
    }


@router.get("/rules")
def rule_catalog():
    return {
        "count": len(rule_registry.all()),
        "rules": rule_registry.all(),
    }


@router.get("/services")
def service_catalog():
    return {
        "count": len(engine.services.all()),
        "services": engine.services.catalog(),
    }


@router.post("/understand")
def understand(request: StartCaseRequest):
    return understanding_engine.understand(
        request.objective,
        request.customer_type,
        request.jurisdiction,
    ).as_dict()


@router.post("/requirements")
def discover_requirements(request: StartCaseRequest):
    requirements = requirements_engine.discover(
        request.objective,
        request.customer_type,
        request.jurisdiction,
        request.inputs,
    )
    required_documents = requirements_engine.document_request(requirements)
    submitted = set(request.inputs.get("documents", []))
    missing = [doc for doc in required_documents["documents"] if doc not in submitted]
    return {
        "requirements": [r.__dict__ for r in requirements],
        "documents": required_documents["documents"],
        "submitted_documents": sorted(submitted),
        "missing_documents": missing,
        "ready_to_execute": not missing,
    }


@router.post("/cases")
def start_case(request: StartCaseRequest, principal: Principal = Depends(require_principal)):
    understanding = understanding_engine.understand(
        request.objective,
        request.customer_type,
        request.jurisdiction,
    )
    requirements = requirements_engine.discover(
        request.objective,
        request.customer_type,
        request.jurisdiction,
        request.inputs,
    )
    required_documents = requirements_engine.document_request(requirements)
    submitted = set(request.inputs.get("documents", []))
    missing = [doc for doc in required_documents["documents"] if doc not in submitted]

    if understanding.service_id is None or understanding.ambiguous:
        return {
            "status": "needs_clarification",
            "objective": request.objective,
            "understanding": understanding.as_dict(),
            "candidates": understanding.candidates,
            "requirements": [r.__dict__ for r in requirements],
        }

    if missing:
        return {
            "status": "needs_documents",
            "objective": request.objective,
            "understanding": understanding.as_dict(),
            "requirements": [r.__dict__ for r in requirements],
            "documents": required_documents["documents"],
            "missing_documents": missing,
        }

    case = engine.create_case(
        request.objective,
        request.customer_type,
        request.jurisdiction,
        {**request.inputs, "enforce_intake_gate": True},
        owner_user_id=principal.subject,
        tenant_id=principal.tenant_id or principal.subject,
    )
    case.requirements = [r.__dict__ for r in requirements]
    case = engine.execute_until_pause(case.case_id)
    return serialize(case)


def _authorize_case(case, principal: Principal) -> None:
    if principal.auth_mode == "none" or principal.role.lower() == "admin":
        return
    same_owner = case.owner_user_id and case.owner_user_id == principal.subject
    same_tenant = case.tenant_id and principal.tenant_id and case.tenant_id == principal.tenant_id
    if principal.role.lower() in {"officer", "department_admin"} and same_tenant:
        return
    if same_owner and (not case.tenant_id or not principal.tenant_id or same_tenant):
        return
    raise HTTPException(status_code=404, detail="Case not found")


@router.get("/cases")
def list_cases(
    status: str | None = None,
    limit: int = 50,
    principal: Principal = Depends(require_principal),
):
    if principal.role.lower() == "admin" or principal.auth_mode == "none":
        return {"cases": engine.store.list(status=status, limit=limit)}
    if principal.role.lower() in {"officer", "department_admin"} and principal.tenant_id:
        return {"cases": engine.store.list(tenant_id=principal.tenant_id, status=status, limit=limit)}
    return {"cases": engine.store.list(owner_user_id=principal.subject, status=status, limit=limit)}


@router.post("/cases/{case_id}/resume")
def resume_case(case_id: str, principal: Principal = Depends(require_principal)):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        return serialize(engine.execute_until_pause(case_id))
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.get("/cases/{case_id}/events")
def case_events(case_id: str, principal: Principal = Depends(require_principal)):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        return {"case_id": case_id, "events": engine.store.events_for(case_id)}
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.get("/cases/{case_id}")
def get_case(case_id: str, principal: Principal = Depends(require_principal)):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        return serialize(case)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.post("/cases/{case_id}/human/{task_id}")
def human_decision(case_id: str, task_id: str, request: HumanDecisionRequest, principal: Principal = Depends(require_role("officer", "admin"))):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        decision = "approved" if request.approved else "rejected"
        case = engine.complete_human_task(case_id, task_id, decision, request.note or "")
        return serialize(case)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case or task not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
