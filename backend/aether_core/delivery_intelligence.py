"""Delivery intelligence primitives for developer and contractor workflows.

This module is deliberately deterministic and advisory. It does not invent
jurisdictional rules, approve bids, certify construction quality, or authorize
payments. Findings are only as reliable as the evidence supplied by the caller.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    title: str
    message: str
    evidence_needed: tuple[str, ...] = ()
    blocks_progress: bool = False


def _decimal(value: Any) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        parsed = Decimal(str(value))
        return parsed if parsed.is_finite() else None
    except (InvalidOperation, ValueError, TypeError):
        return None


def assess_delivery_risks(project: Mapping[str, Any]) -> dict[str, Any]:
    """Return explainable risk findings from supplied project facts.

    Accepted optional fields:
      budget, committed_cost, forecast_cost, contingency_percent,
      planned_finish (ISO date), forecast_finish (ISO date),
      permits (list of {name, status, evidence_ref?}),
      milestones (list of {name, status, due_date?, owner?}),
      payment_claims (list of {amount, evidence_complete, due_date?, status?}),
      dependencies (list of {name, status, owner?}).

    Missing values are reported as unknown rather than treated as safe.
    """
    findings: list[Finding] = []
    budget = _decimal(project.get("budget"))
    committed = _decimal(project.get("committed_cost"))
    forecast = _decimal(project.get("forecast_cost"))
    contingency = _decimal(project.get("contingency_percent"))

    # Assess the budget baseline and cost forecast independently: one missing
    # field must not hide the uncertainty in another field.
    if budget is None:
        findings.append(Finding(
            "budget_unknown", "info", "Budget baseline missing",
            "A budget variance cannot be calculated until an approved budget is supplied.",
            ("approved_budget",),
        ))
    elif budget <= 0:
        findings.append(Finding(
            "invalid_budget", "warning", "Budget baseline is invalid",
            "Budget must be greater than zero before a percentage variance can be calculated.",
            ("approved_budget",),
        ))

    if forecast is None:
        findings.append(Finding(
            "forecast_unknown", "warning", "Cost-to-complete unknown",
            "No forecast cost was supplied, so final cost exposure cannot be assessed.",
            ("cost_to_complete_forecast",),
        ))
    elif budget is not None and budget > 0:
        variance = (forecast - budget) / budget * Decimal("100")
        if variance > 0:
            severity = "critical" if variance >= Decimal("10") else "warning"
            findings.append(Finding(
                "forecast_over_budget", severity, "Forecast exceeds budget",
                f"Forecast is {variance.quantize(Decimal('0.1'))}% above the supplied budget.",
                ("forecast_cost_breakdown", "approved_change_orders"),
                severity == "critical",
            ))
        elif variance < 0:
            findings.append(Finding(
                "forecast_under_budget", "info", "Forecast below budget",
                "Forecast is below the supplied budget; confirm scope and committed costs are complete.",
                ("latest_cost_report",),
            ))

    if budget is not None and committed is not None and budget > 0 and committed > budget:
        findings.append(Finding(
            "commitments_exceed_budget", "critical", "Commitments exceed budget",
            "Recorded commitments already exceed the supplied budget baseline.",
            ("commitment_register", "approved_budget_revision"),
            True,
        ))

    if contingency is not None and contingency < 0:
        findings.append(Finding(
            "invalid_contingency", "warning", "Contingency input is invalid",
            "Contingency percentage cannot be negative; correct the input before relying on risk outputs.",
            ("contingency_assumption",),
        ))

    planned_finish = _parse_date(project.get("planned_finish"))
    forecast_finish = _parse_date(project.get("forecast_finish"))
    if project.get("planned_finish") and planned_finish is None:
        findings.append(Finding(
            "invalid_planned_finish", "warning", "Planned finish date is invalid",
            "Use an ISO date (YYYY-MM-DD) for the planned finish date.",
        ))
    if project.get("forecast_finish") and forecast_finish is None:
        findings.append(Finding(
            "invalid_forecast_finish", "warning", "Forecast finish date is invalid",
            "Use an ISO date (YYYY-MM-DD) for the forecast finish date.",
        ))
    if planned_finish and forecast_finish and forecast_finish > planned_finish:
        delay_days = (forecast_finish - planned_finish).days
        findings.append(Finding(
            "forecast_schedule_slip", "critical" if delay_days >= 30 else "warning",
            "Forecast finish is late",
            f"Forecast completion is {delay_days} calendar days after the supplied planned finish.",
            ("updated_critical_path", "recovery_plan", "owner_and_due_date_for_mitigations"),
            delay_days >= 30,
        ))

    permits = _as_records(project.get("permits"))
    for permit in permits:
        status = str(permit.get("status", "unknown")).strip().lower()
        name = str(permit.get("name") or "Unnamed permit")
        if status in {"pending", "missing", "rejected", "expired", "unknown", ""}:
            findings.append(Finding(
                "permit_not_cleared", "critical" if status in {"rejected", "expired"} else "warning",
                f"Permit needs attention: {name}",
                f"Permit status is '{status or 'unknown'}'; verify against the competent authority and current project scope.",
                ("permit_status_source", "application_or_certificate_reference"),
                status in {"rejected", "expired"},
            ))
        elif not permit.get("evidence_ref"):
            findings.append(Finding(
                "permit_evidence_missing", "warning", f"Permit evidence missing: {name}",
                "A status was supplied but no evidence reference was attached.",
                ("permit_document_or_authority_receipt",),
            ))

    for milestone in _as_records(project.get("milestones")):
        status = str(milestone.get("status", "unknown")).strip().lower()
        name = str(milestone.get("name") or "Unnamed milestone")
        owner = milestone.get("owner")
        due = _parse_date(milestone.get("due_date"))
        if status not in {"complete", "completed", "accepted", "closed"}:
            if not owner:
                findings.append(Finding(
                    "milestone_unowned", "warning", f"Milestone has no owner: {name}",
                    "Assign one accountable owner so the next action cannot disappear between teams.",
                    ("named_accountable_owner",),
                ))
            if due and due < date.today():
                findings.append(Finding(
                    "milestone_overdue", "critical", f"Milestone overdue: {name}",
                    f"Milestone due date was {due.isoformat()} and it is not marked complete.",
                    ("completion_evidence_or_recovery_action",),
                    True,
                ))

    for dependency in _as_records(project.get("dependencies")):
        status = str(dependency.get("status", "unknown")).strip().lower()
        if status not in {"complete", "completed", "ready", "cleared"}:
            name = str(dependency.get("name") or "Unnamed dependency")
            findings.append(Finding(
                "dependency_blocked", "warning", f"Dependency unresolved: {name}",
                "The dependency is not marked ready; downstream dates may be unreliable.",
                ("dependency_status_evidence", "accountable_owner", "next_action_date"),
            ))

    for claim in _as_records(project.get("payment_claims")):
        status = str(claim.get("status", "submitted")).strip().lower()
        if status not in {"paid", "settled", "rejected", "cancelled"} and claim.get("evidence_complete") is not True:
            findings.append(Finding(
                "payment_claim_evidence_incomplete", "warning", "Payment claim lacks complete evidence",
                "Do not infer that a claim is payable. Identify the contractually required evidence and obtain the responsible reviewer's decision.",
                ("signed_measurement_or_milestone_record", "invoice", "required_approvals"),
            ))

    severity_rank = {"critical": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda item: (severity_rank.get(item.severity, 3), item.code, item.title))
    blockers = sum(1 for item in findings if item.blocks_progress)
    return {
        "schema_version": "1.0",
        "mode": "advisory",
        "source_data_complete": bool(project),
        "summary": {
            "finding_count": len(findings),
            "critical_count": sum(1 for item in findings if item.severity == "critical"),
            "warning_count": sum(1 for item in findings if item.severity == "warning"),
            "progress_blocker_count": blockers,
        },
        "findings": [asdict(item) for item in findings],
        "limitations": [
            "Findings are based only on facts supplied to this function.",
            "No permit, legal, engineering, safety, contractual, or payment decision is made.",
            "Jurisdiction-specific rules must be sourced, versioned, and verified separately.",
            "A missing finding is not proof that a project is compliant or risk-free.",
        ],
    }


def _parse_date(value: Any) -> date | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


def _as_records(value: Any) -> list[Mapping[str, Any]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return [item for item in value if isinstance(item, Mapping)]
