from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List


AMOUNT_KEYS = (
    "fee_due_minor",
    "demand_minor",
    "dues_minor",
    "amount_due_minor",
)


def reconcile_financial_position(
    *,
    task_results: Dict[str, Any],
    payment_records: List[Dict[str, Any]],
) -> Dict[str, Any]:
    demand_values: List[int] = []
    sources: List[str] = []

    for source_name, result in task_results.items():
        if not isinstance(result, dict):
            continue
        for key in AMOUNT_KEYS:
            value = result.get(key)
            if value is None:
                continue
            try:
                demand_values.append(int(value))
                sources.append(f"{source_name}:{key}")
            except (TypeError, ValueError):
                continue

    known_demand = max(demand_values) if demand_values else None
    succeeded = [
        item for item in payment_records
        if item.get("status") == "succeeded"
    ]
    paid_total = sum(int(item.get("amount_minor") or 0) for item in succeeded)

    payment_ids = [str(item.get("provider_payment_id") or item.get("payment_id") or "") for item in succeeded]
    duplicate_payment_ids = [
        value for value, count in Counter(payment_ids).items()
        if value and count > 1
    ]

    unlinked = [
        item for item in succeeded
        if not item.get("case_id")
    ]

    if known_demand is None:
        status = "awaiting_authoritative_demand"
    elif paid_total < known_demand:
        status = "payment_due"
    elif paid_total > known_demand:
        status = "overpayment_or_duplicate_review"
    else:
        status = "balanced"

    exceptions = []
    if duplicate_payment_ids:
        exceptions.append({
            "code": "DUPLICATE_PAYMENT_REFERENCE",
            "references": duplicate_payment_ids,
        })
    if unlinked:
        exceptions.append({
            "code": "UNLINKED_PAYMENT",
            "count": len(unlinked),
        })

    return {
        "known_demand_minor": known_demand,
        "paid_minor": paid_total,
        "balance_minor": None if known_demand is None else known_demand - paid_total,
        "status": status,
        "demand_sources": sorted(set(sources)),
        "exceptions": exceptions,
        "next_actions": (
            ["reconcile authoritative demand", "issue/collect applicable balance"]
            if status == "payment_due"
            else ["review duplicate/overpayment and preserve payment audit trail"]
            if status == "overpayment_or_duplicate_review"
            else ["close financial reconciliation"]
            if status == "balanced"
            else ["obtain authoritative demand/fee record"]
        ),
        "safety": {
            "fee_rule_not_invented": True,
            "payment_not_marked_satisfied_without_provider_confirmation": True,
        },
    }
