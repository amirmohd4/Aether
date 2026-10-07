from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .api_models import HumanDecisionRequest, StartCaseRequest
from .engine import AetherExecutionEngine
from .requirements_engine import RequirementEngine

router = APIRouter(prefix="/api/aether/v2", tags=["Aether V2"])
engine = AetherExecutionEngine()
requirements_engine = RequirementEngine()


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
                "idempotency_key": state.idempotency_key,
            }
            for task_id, state in case.tasks.items()
        },
        "human_actions": case.human_actions,
        "exceptions": case.exceptions,
        "evidence": case.evidence,
        "outcome": case.outcome,
        "execution_events": case.execution_events[-50:],
    }


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
def start_case(request: StartCaseRequest):
    requirements = requirements_engine.discover(
        request.objective,
        request.customer_type,
        request.jurisdiction,
        request.inputs,
    )
    required_documents = requirements_engine.document_request(requirements)
    submitted = set(request.inputs.get("documents", []))
    missing = [doc for doc in required_documents["documents"] if doc not in submitted]

    # Aether should not launch downstream government work when required intake is incomplete.
    if missing:
        return {
            "status": "needs_documents",
            "objective": request.objective,
            "requirements": [r.__dict__ for r in requirements],
            "documents": required_documents["documents"],
            "missing_documents": missing,
        }

    case = engine.create_case(
        request.objective,
        request.customer_type,
        request.jurisdiction,
        request.inputs,
    )
    case.requirements = [r.__dict__ for r in requirements]
    case = engine.execute_until_pause(case.case_id)
    return serialize(case)


@router.get("/cases/{case_id}")
def get_case(case_id: str):
    try:
        return serialize(engine.get_case(case_id))
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.post("/cases/{case_id}/human/{task_id}")
def human_decision(case_id: str, task_id: str, request: HumanDecisionRequest):
    try:
        decision = "approved" if request.approved else "rejected"
        case = engine.complete_human_task(case_id, task_id, decision, request.note or "")
        return serialize(case)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case or task not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
