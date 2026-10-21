"""Deterministic administrative action planner.

Creates suggested work items from explainable risk findings and open handoffs.
It does not submit filings, contact authorities, approve claims, or mutate cases.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence


_ACTIONS = {
    "budget_unknown": ("collect_approved_budget", "project_controls", "normal"),
    "forecast_unknown": ("request_cost_to_complete_forecast", "project_controls", "high"),
    "forecast_over_budget": ("prepare_cost_variance_and_change_order_review", "project_controls", "high"),
    "commitments_exceed_budget": ("escalate_commitment_register", "finance", "critical"),
    "forecast_schedule_slip": ("prepare_schedule_recovery_plan", "project_controls", "high"),
    "permit_not_cleared": ("verify_permit_status_and_source_evidence", "permits_or_compliance", "high"),
    "permit_evidence_missing": ("request_permit_receipt_or_certificate", "permits_or_compliance", "normal"),
    "milestone_unowned": ("assign_accountable_milestone_owner", "project_controls", "normal"),
    "milestone_overdue": ("request_completion_evidence_or_recovery_action", "delivery_department", "critical"),
    "dependency_blocked": ("assign_dependency_owner_and_next_action", "dependency_owner", "high"),
    "payment_claim_evidence_incomplete": ("assemble_missing_payment_claim_evidence", "commercial_or_finance", "high"),
}


def _stable_id(payload: Mapping[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return "act_" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def plan_administrative_actions(
    case_id: str,
    findings: Sequence[Mapping[str, Any]],
    handoffs: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Return deduplicated, auditable proposed actions; callers decide whether to enqueue."""
    actions: list[dict[str, Any]] = []
    seen: set[str] = set()

    for finding in findings:
        code = str(finding.get("code", ""))
        mapping = _ACTIONS.get(code)
        if not mapping:
            continue
        action_type, department, priority = mapping
        action = {
            "case_id": case_id,
            "action_type": action_type,
            "source_finding": code,
            "title": str(finding.get("title") or action_type.replace("_", " ").title()),
            "department": department,
            "priority": priority,
            "required_evidence": list(finding.get("evidence_needed") or []),
            "requires_human_decision": code in {
                "commitments_exceed_budget", "forecast_over_budget",
                "forecast_schedule_slip", "permit_not_cleared",
                "milestone_overdue", "payment_claim_evidence_incomplete",
            },
            "execution_mode": "proposed_not_enqueued",
        }
        action["idempotency_key"] = _stable_id(action)
        if action["idempotency_key"] not in seen:
            seen.add(action["idempotency_key"])
            actions.append(action)

    for handoff in handoffs:
        if not handoff.get("blocked_by") and not handoff.get("error"):
            continue
        action = {
            "case_id": case_id,
            "action_type": "resolve_cross_department_handoff",
            "source_task_id": handoff.get("task_id"),
            "title": f"Resolve handoff: {handoff.get('task') or handoff.get('task_id')}",
            "department": handoff.get("department") or "unassigned",
            "priority": "high" if handoff.get("blocked_by") else "critical",
            "required_evidence": [],
            "blocked_by": list(handoff.get("blocked_by") or []),
            "requires_human_decision": bool(handoff.get("human_authority_required")),
            "execution_mode": "proposed_not_enqueued",
        }
        action["idempotency_key"] = _stable_id(action)
        if action["idempotency_key"] not in seen:
            seen.add(action["idempotency_key"])
            actions.append(action)

    actions.sort(key=lambda item: (
        {"critical": 0, "high": 1, "normal": 2}.get(item["priority"], 3),
        item["department"],
        item["action_type"],
    ))
    return {
        "count": len(actions),
        "actions": actions,
        "mode": "recommend_only",
        "note": "Actions are proposed, not queued or executed. Enqueue only after tenant authorization, policy checks, ownership assignment, and any required human approval.",
    }
