from __future__ import annotations

from typing import Any, Dict, List


IDENTIFIER_FIELDS = (
    "registration_id",
    "certificate_reference",
    "company_id",
    "property_id",
    "parcel_id",
    "project_id",
    "gstin",
    "pan",
    "tax_id",
    "beneficiary_id",
    "claim_id",
    "employee_id",
)


def find_duplicate_cases(store, case, limit: int = 50) -> Dict[str, Any]:
    candidates = store.list(
        tenant_id=case.tenant_id,
        owner_user_id=case.owner_user_id,
        limit=max(1, min(limit, 100)),
    )

    current_inputs = case.inputs or {}
    current_identifiers = {
        field: str(current_inputs.get(field)).strip()
        for field in IDENTIFIER_FIELDS
        if current_inputs.get(field) is not None
    }

    matches: List[Dict[str, Any]] = []
    for summary in candidates:
        if summary.get("case_id") == case.case_id:
            continue
        if summary.get("service_id") != case.service_id:
            continue

        try:
            other = store.get(summary["case_id"])
        except Exception:
            continue

        other_inputs = other.inputs or {}
        other_identifiers = {
            field: str(other_inputs.get(field)).strip()
            for field in IDENTIFIER_FIELDS
            if other_inputs.get(field) is not None
        }
        shared = {
            field: value
            for field, value in current_identifiers.items()
            if other_identifiers.get(field) == value
        }

        objective_same = str(other.objective).strip().lower() == str(case.objective).strip().lower()
        if shared:
            matches.append({
                "case_id": other.case_id,
                "status": other.status,
                "shared_identifiers": sorted(shared),
                "confidence": "high" if len(shared) >= 2 else "medium",
                "objective_same": objective_same,
                "action": "review existing case before creating duplicate work",
            })
        elif objective_same and not current_identifiers:
            matches.append({
                "case_id": other.case_id,
                "status": other.status,
                "shared_identifiers": [],
                "confidence": "low",
                "objective_same": True,
                "action": "review possible duplicate; identifiers unavailable",
            })

    return {
        "duplicate_candidates": matches[:20],
        "duplicate_candidate_count": len(matches),
        "safe_action": "flag_for_review",
        "auto_merge": False,
        "auto_close": False,
        "reason": "Duplicate detection prevents parallel government work while preserving human control over case identity.",
    }
