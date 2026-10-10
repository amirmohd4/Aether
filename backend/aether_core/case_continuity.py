from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List

from .case_store import DatabaseCaseStore
from .domain import TaskStatus


REUSABLE_FIELDS = {
    "owner_name",
    "applicant_name",
    "company_name",
    "company_id",
    "property_id",
    "parcel_id",
    "project_id",
    "registration_id",
    "tax_id",
    "gstin",
    "pan",
    "address",
}


def build_continuity_review(
    tenant_id: str | None,
    owner_user_id: str | None,
    service_id: str | None,
    current_inputs: Dict[str, Any] | None = None,
    limit: int = 20,
) -> Dict[str, Any]:
    if not tenant_id and not owner_user_id:
        return {
            "status": "unavailable",
            "reason": "A tenant or owner scope is required before prior-case continuity can be considered.",
        }

    store = DatabaseCaseStore()
    summaries = store.list(
        tenant_id=tenant_id,
        owner_user_id=owner_user_id,
        limit=max(1, min(limit, 50)),
    )
    related = [
        item for item in summaries
        if service_id and item.get("service_id") == service_id
        and item.get("status") in {"completed", "waiting_for_human", "waiting"}
    ]

    reusable: Dict[str, Dict[str, Any]] = {}
    exception_codes: Counter[str] = Counter()
    prior_cases: List[Dict[str, Any]] = []

    for summary in related:
        case_id = summary.get("case_id")
        try:
            case = store.get(case_id)
        except Exception:
            continue
        fields: Dict[str, Any] = {}
        for task in case.tasks.values():
            if task.status != TaskStatus.COMPLETED or not isinstance(task.result, dict):
                continue
            for field in REUSABLE_FIELDS:
                if task.result.get(field) is not None and field not in fields:
                    fields[field] = task.result[field]
            for exception in task.result.get("findings", []) or []:
                if isinstance(exception, dict) and exception.get("code"):
                    exception_codes[str(exception["code"])] += 1

        for exception in case.exceptions:
            if exception.get("type"):
                exception_codes[str(exception["type"])] += 1

        if fields:
            for field, value in fields.items():
                if field not in reusable:
                    reusable[field] = {
                        "value": value,
                        "source_case_id": case.case_id,
                        "reuse_allowed": False,
                        "requires_user_confirmation": True,
                    }

        prior_cases.append({
            "case_id": case.case_id,
            "status": case.status,
            "updated_at": case.updated_at,
            "verified_field_count": len(fields),
        })

    warnings = [
        {
            "type": "recurring_exception",
            "code": code,
            "occurrences": count,
            "action": "Run the corresponding preflight check before submission.",
        }
        for code, count in exception_codes.most_common(10)
    ]

    return {
        "status": "available" if prior_cases else "no_related_cases",
        "related_case_count": len(prior_cases),
        "prior_cases": prior_cases[:20],
        "reusable_verified_fields": reusable,
        "preflight_warnings": warnings,
        "policy": {
            "auto_copy": False,
            "document_auto_transfer": False,
            "explicit_user_confirmation_required": True,
            "tenant_and_owner_scope_required": True,
        },
        "current_input_fields": sorted((current_inputs or {}).keys()),
    }
