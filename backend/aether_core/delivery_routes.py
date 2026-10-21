"""Project delivery intelligence API for developer and contractor workflows.

This router composes existing Aether cases with deterministic risk findings.
It never calls an authority, approves a permit, certifies construction, or
represents synthetic connector output as an official result.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from .admin_automation import plan_administrative_actions
from .admin_action_queue import AdminActionQueue
from .delivery_intelligence import assess_delivery_risks
from .engine import engine
from .routes import _authorize_case
from .security import Principal, require_role, require_scope

router = APIRouter(prefix="/api/aether/v2", tags=["Delivery Intelligence"])


PLAYBOOKS = [
    {
        "id": "developer-project-readiness",
        "name": "Developer project readiness",
        "audience": ["developer", "real_estate_operator", "project_owner"],
        "departments": ["land_records", "planning", "municipal", "utilities", "environment", "fire", "finance"],
        "stages": [
            "scope_and_jurisdiction_intake",
            "evidence_and_title_checks",
            "planning_and_statutory_requirements",
            "design_and_utility_dependencies",
            "finance_and_procurement_conditions",
            "inspection_and_completion_evidence",
        ],
        "automation": ["missing_evidence_detection", "dependency_tracking", "deadline_tracking", "cost_and_schedule_risk"],
        "authority_boundary": "Official approvals, title determinations, inspections, and statutory decisions remain with authorized authorities.",
    },
    {
        "id": "contractor-tender-to-payment",
        "name": "Contractor tender-to-payment",
        "audience": ["contractor", "epc", "subcontractor"],
        "departments": ["procurement", "engineering", "site_operations", "safety", "tax_compliance", "client_acceptance", "finance"],
        "stages": [
            "tender_and_addenda_intake",
            "eligibility_and_bid_readiness",
            "scope_boq_and_revision_control",
            "mobilisation_and_expiring_evidence",
            "milestone_measurement_and_acceptance",
            "invoice_and_payment_claim_evidence",
        ],
        "automation": ["deadline_and_expiry_alerts", "missing_attachment_checks", "version_difference_review", "payment_pack_assembly"],
        "authority_boundary": "Bid submission, engineering sign-off, contractual entitlement, and payment release require authorized human or system controls.",
    },
    {
        "id": "developer-api-integration",
        "name": "Developer API integration",
        "audience": ["software_developer", "proptech", "fintech", "enterprise_integrator"],
        "departments": ["identity", "case_orchestration", "connector_runtime", "evidence", "notifications", "audit"],
        "stages": [
            "sandbox_and_credentials",
            "objective_and_requirements",
            "idempotent_case_execution",
            "callback_and_status_reconciliation",
            "audit_and_error_recovery",
        ],
        "automation": ["schema_validation", "safe_retries", "request_tracing", "webhook_reconciliation"],
        "authority_boundary": "Credentials and scopes must be tenant-authorized; live external actions require approved connectors.",
    },
]


@router.get("/delivery-playbooks")
def delivery_playbooks(principal: Principal = Depends(require_scope("cases:read"))):
    """Return reusable cross-department playbook definitions."""
    return {
        "count": len(PLAYBOOKS),
        "playbooks": PLAYBOOKS,
        "execution_model": "objective -> requirements -> dependency graph -> parallel work -> evidence verification -> reconciliation -> outcome or authorized review",
        "mode": "catalogue_only",
    }


@router.get("/cases/{case_id}/delivery-intelligence")
def case_delivery_intelligence(
    case_id: str,
    principal: Principal = Depends(require_scope("cases:read")),
):
    """Summarize risks, handoffs, and proposed administrative actions for a case."""
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")

    raw = case.inputs.get("delivery_project")
    project = dict(raw) if isinstance(raw, dict) else {}
    fields = (
        "budget", "committed_cost", "forecast_cost", "contingency_percent",
        "planned_finish", "forecast_finish", "permits", "milestones",
        "payment_claims", "dependencies",
    )
    for field in fields:
        if field not in project and field in case.inputs:
            project[field] = case.inputs[field]

    task_map = getattr(case, "tasks", {}) or {}
    task_rows = []
    for task_id, task in task_map.items():
        definition = getattr(task, "definition", None)
        status_obj = getattr(task, "status", "unknown")
        status = getattr(status_obj, "value", status_obj)
        dependencies = list(getattr(definition, "dependencies", []) or [])
        department = getattr(definition, "department", "unassigned")
        name = getattr(definition, "name", task_id)
        task_rows.append({
            "task_id": task_id,
            "name": name,
            "department": department,
            "status": str(status),
            "dependencies": dependencies,
            "authority_required": bool(getattr(definition, "authority_required", False)),
            "physical_action": bool(getattr(definition, "physical_action", False)),
            "error": getattr(task, "error", None),
        })

    completed_values = {"completed", "complete", "accepted", "closed"}
    handoffs = []
    by_id = {row["task_id"]: row for row in task_rows}
    for row in task_rows:
        if row["status"].lower() in completed_values:
            continue
        blocked_by = [
            dep for dep in row["dependencies"]
            if dep in by_id and by_id[dep]["status"].lower() not in completed_values
        ]
        handoffs.append({
            "task_id": row["task_id"],
            "task": row["name"],
            "department": row["department"],
            "status": row["status"],
            "blocked_by": blocked_by,
            "next_action": (
                "Resolve or review upstream dependencies"
                if blocked_by
                else "Review task status, required evidence, and assigned owner"
            ),
            "human_authority_required": row["authority_required"] or row["physical_action"],
            "error": row["error"],
        })

    risks = assess_delivery_risks(project)
    admin_plan = plan_administrative_actions(
        case.case_id,
        risks["findings"],
        handoffs,
    )
    return {
        "case_id": case.case_id,
        "objective": case.objective,
        "service": {"id": case.service_id, "name": case.service_name, "outcome": case.service_outcome},
        "jurisdiction": case.jurisdiction,
        "case_status": case.status,
        "mode": "advisory",
        "risk_assessment": risks,
        "cross_department_orchestration": {
            "department_count": len({row["department"] for row in task_rows}),
            "task_count": len(task_rows),
            "open_handoff_count": len(handoffs),
            "human_authority_count": sum(1 for row in handoffs if row["human_authority_required"]),
            "handoffs": handoffs,
        },
        "administrative_action_plan": admin_plan,
        "limitations": [
            "This view uses only case inputs and recorded task state; it does not independently verify official systems.",
            "Administrative actions are proposals only; they are not queued or executed by this endpoint.",
            "A task marked complete is not proof that an external authority accepted an application unless source-backed evidence confirms it.",
            "Unknown or absent financial and schedule inputs are not treated as safe.",
        ],
    }



_action_queue = AdminActionQueue()


@router.post("/cases/{case_id}/administrative-actions/{action_key}/enqueue")
def enqueue_administrative_action(
    case_id: str,
    action_key: str,
    principal: Principal = Depends(require_scope("cases:write")),
):
    """Persist a safe internal work item; sensitive actions wait for a second reviewer."""
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")

    intelligence = case_delivery_intelligence(case_id, principal)
    action = next(
        (item for item in intelligence["administrative_action_plan"]["actions"]
         if item.get("idempotency_key") == action_key),
        None,
    )
    if action is None:
        raise HTTPException(status_code=404, detail="Action proposal not found or no longer current")
    tenant_id = case.tenant_id or principal.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=403, detail="A tenant-bound case is required")
    try:
        result = _action_queue.enqueue(
            tenant_id=tenant_id,
            case_id=case_id,
            action=action,
            requested_by=principal.subject,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {
        "action": result,
        "message": (
            "Queued for internal dispatch"
            if result["status"] == "queued"
            else "Awaiting approval by a different authorized reviewer"
        ),
        "external_effect": False,
    }


@router.post("/cases/{case_id}/administrative-actions/{action_id}/approve")
def approve_administrative_action(
    case_id: str,
    action_id: str,
    principal: Principal = Depends(require_role("officer", "department_admin", "admin")),
):
    """Second-person approval releases only an internal work item, never a statutory decision."""
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")
    tenant_id = case.tenant_id or principal.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=403, detail="A tenant-bound case is required")
    try:
        existing = _action_queue.get(action_id=action_id, tenant_id=tenant_id)
        if existing["case_id"] != case_id:
            raise HTTPException(status_code=404, detail="Action not found")
        result = _action_queue.approve(
            action_id=action_id, tenant_id=tenant_id, approver=principal.subject
        )
        return {"action": result, "external_effect": False}
    except KeyError:
        raise HTTPException(status_code=404, detail="Action not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@router.get("/cases/{case_id}/administrative-actions")
def list_administrative_actions(
    case_id: str,
    principal: Principal = Depends(require_scope("cases:read")),
):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")
    tenant_id = case.tenant_id or principal.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=403, detail="A tenant-bound case is required")
    return {
        "case_id": case_id,
        "actions": _action_queue.list_for_case(case_id=case_id, tenant_id=tenant_id),
        "work_items": _action_queue.list_work_items_for_case(case_id=case_id, tenant_id=tenant_id),
        "execution_boundary": "internal_work_items_only",
    }


@router.post("/admin-actions/dispatch-worker")
def dispatch_administrative_actions(request: Request, limit: int = 20):
    """Scheduler/worker endpoint protected by a dedicated secret, not user auth."""
    import hmac
    import os

    expected = os.getenv("AETHER_AUTOMATION_WORKER_TOKEN", "")
    supplied = request.headers.get("X-Aether-Automation-Token", "")
    if not expected:
        raise HTTPException(status_code=503, detail="Administrative automation worker is not configured")
    if not supplied or not hmac.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="Invalid worker credential")
    return _action_queue.dispatch(limit=limit)
