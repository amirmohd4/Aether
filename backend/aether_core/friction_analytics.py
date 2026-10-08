from __future__ import annotations

from typing import Any, Dict, Iterable


def analyze_case_friction(case) -> Dict[str, Any]:
    """Estimate avoidable citizen and employee friction from observable case state.

    These are operational heuristics, not claims about real government time.
    They are designed to identify where Aether should remove repeat work.
    """
    tasks = list(case.tasks.values())
    document_inputs = case.inputs.get("documents") or []
    document_count = len(document_inputs)

    attempts = sum(max(0, int(task.attempts or 0) - 1) for task in tasks)
    connector_errors = sum(
        1 for task in tasks
        if isinstance(task.error, str)
        and any(token in task.error.lower() for token in ("connector", "portal", "timeout", "http"))
    )
    human_boundaries = sum(
        1 for task in tasks
        if task.definition.authority_required or task.definition.physical_action
    )
    completed_admin = sum(
        1 for task in tasks
        if task.status.value == "completed" and task.definition.department.lower() == "aether"
    )
    handoff_tasks = sum(
        1 for task in tasks
        if "handoff" in task.definition.id or "correspond" in task.definition.id
    )
    missing_docs = 0
    for req in case.requirements:
        for document in req.get("documents", []):
            if document not in document_inputs:
                missing_docs += 1

    citizen_score = min(
        100,
        document_count * 3
        + missing_docs * 8
        + human_boundaries * 8
        + handoff_tasks * 5
        + connector_errors * 10
        + attempts * 4,
    )
    employee_score = min(
        100,
        completed_admin * 2
        + handoff_tasks * 8
        + attempts * 5
        + connector_errors * 10
        + human_boundaries * 7
        + missing_docs * 3,
    )

    friction_sources = []
    if missing_docs:
        friction_sources.append({
            "type": "missing_or_incomplete_evidence",
            "impact": "citizen_and_employee",
            "count": missing_docs,
            "aether_action": "validate once, request only the missing evidence, then resume the affected branch",
        })
    if handoff_tasks:
        friction_sources.append({
            "type": "cross_department_coordination",
            "impact": "employee",
            "count": handoff_tasks,
            "aether_action": "package the request, route it, track response and escalate on SLA risk",
        })
    if connector_errors:
        friction_sources.append({
            "type": "portal_or_connector_failure",
            "impact": "citizen_and_employee",
            "count": connector_errors,
            "aether_action": "preserve prepared work, retry durably and avoid asking the applicant to re-enter data",
        })
    if attempts:
        friction_sources.append({
            "type": "rework",
            "impact": "employee",
            "count": attempts,
            "aether_action": "reuse verified facts and compare only changed evidence on resubmission",
        })
    if human_boundaries:
        friction_sources.append({
            "type": "authority_or_field_boundary",
            "impact": "government",
            "count": human_boundaries,
            "aether_action": "prepare the officer packet and return the result to the graph automatically",
        })

    bottleneck_counts = {
        "applicant": missing_docs,
        "official": 0,
        "statutory_or_field": 0,
        "automation": 0,
        "exception": len(case.exceptions),
    }
    bottleneck_tasks = []
    for task in tasks:
        status = task.status.value
        if status == "human_review":
            bottleneck_counts["statutory_or_field"] += 1
            bottleneck_tasks.append({"task_id": task.definition.id, "owner": task.definition.department, "reason": "human decision or field action"})
        elif status == "blocked":
            bottleneck_counts["official"] += 1
            bottleneck_tasks.append({"task_id": task.definition.id, "owner": task.definition.department, "reason": "upstream prerequisite"})
        elif status in {"pending", "ready", "running"} and task.definition.department.lower() != "aether":
            bottleneck_counts["official"] += 1
            bottleneck_tasks.append({"task_id": task.definition.id, "owner": task.definition.department, "reason": "departmental work pending"})

    top_bottleneck = "applicant" if missing_docs else (
        "statutory_or_field" if bottleneck_counts["statutory_or_field"] else
        "official" if bottleneck_counts["official"] else
        "exception" if case.exceptions else
        "none"
    )

    recovery = {
        "mode": "automatic_recovery",
        "preserve_case_state": True,
        "reenter_user_data": False,
        "ask_user_to_reenter_data": False,
        "retry_failed_connectors": connector_errors > 0,
        "compare_only_changed_evidence": attempts > 0,
        "escalate_sla_risk": bool(case.exceptions),
        "replan_affected_branch": bool(case.exceptions or missing_docs),
    }

    return {
        "citizen_effort_score": citizen_score,
        "employee_effort_score": employee_score,
        "friction_sources": friction_sources[:12],
        "signals": {
            "document_count": document_count,
            "missing_document_count": missing_docs,
            "avoidable_rework_attempts": attempts,
            "connector_or_portal_failures": connector_errors,
            "human_authority_boundaries": human_boundaries,
            "administrative_tasks_completed": completed_admin,
        },
        "recovery_plan": recovery,
        "bottleneck": {
            "top_bucket": top_bottleneck,
            "counts": bottleneck_counts,
            "tasks": bottleneck_tasks[:20],
            "user_message": (
                "Action needed from you: provide the missing evidence."
                if top_bottleneck == "applicant"
                else "Waiting on an authorised government decision or field action."
                if top_bottleneck == "statutory_or_field"
                else "Waiting on the responsible government department; Aether will track the dependency."
                if top_bottleneck == "official"
                else "Aether is handling the remaining automated work."
                if top_bottleneck == "none"
                else "Aether has identified an exception and is preparing recovery."
            ),
        },
        "note": "Friction scores are internal operational heuristics for prioritisation, not measured government service times.",
    }
