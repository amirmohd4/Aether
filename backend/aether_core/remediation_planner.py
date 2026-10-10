from __future__ import annotations

from typing import Any, Dict, List


def build_remediation_plan(
    *,
    deficiencies: List[Dict[str, Any]] | None = None,
    queries: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = []

    for item in deficiencies or []:
        if not isinstance(item, dict):
            continue
        code = str(item.get("code") or "DEFICIENCY")
        applicant_fixable = bool(item.get("applicant_fixable"))
        items.append({
            "code": code,
            "owner": "applicant" if applicant_fixable else "Aether + authorised officer",
            "action": item.get("fix") or item.get("message") or "Review the deficiency and prepare the required evidence.",
            "automation": "prepare_only" if applicant_fixable else "assemble_and_route",
            "user_next_step": item.get("fix") if applicant_fixable else None,
            "blocks_case": True,
        })

    for item in queries or []:
        if not isinstance(item, dict):
            continue
        code = str(item.get("code") or "OTHER_QUERY")
        applicant_fixable = bool(item.get("applicant_fixable"))
        action = item.get("recommended_action") or "Prepare an evidence-backed response."
        items.append({
            "code": code,
            "owner": "applicant" if applicant_fixable else "Aether + authorised officer",
            "action": action,
            "automation": "draft_response" if applicant_fixable else "assemble_and_review",
            "user_next_step": action if applicant_fixable else None,
            "blocks_case": True,
        })

    # Stable ordering prevents operators seeing a different correction plan
    # every time the case is refreshed.
    priority = {
        "MISSING_DOCUMENT": 1,
        "IDENTITY_MISMATCH": 2,
        "DATA_MISMATCH": 2,
        "PAYMENT_SHORTFALL": 3,
        "FORM_VALIDATION": 3,
        "JURISDICTION": 4,
        "FIELD_VERIFICATION": 5,
        "SYSTEM_ERROR": 6,
    }
    items.sort(key=lambda item: (priority.get(item["code"], 99), item["code"]))

    return {
        "action_count": len(items),
        "actions": items[:50],
        "status": "action_required" if items else "clear",
        "principle": "convert every deficiency/query into one concrete next action and preserve the case state",
    }
