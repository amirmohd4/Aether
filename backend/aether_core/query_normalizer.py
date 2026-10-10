from __future__ import annotations

from typing import Any, Dict, List


QUERY_REASON_RULES = [
    (
        "MISSING_DOCUMENT",
        ("missing document", "document required", "upload", "attach", "supporting document"),
        True,
        "provide the missing evidence",
    ),
    (
        "IDENTITY_MISMATCH",
        ("name mismatch", "identity mismatch", "aadhaar mismatch", "pan mismatch", "kyc mismatch"),
        True,
        "correct or reconcile identity fields",
    ),
    (
        "DATA_MISMATCH",
        ("mismatch", "inconsistent", "does not match", "discrepancy", "difference"),
        False,
        "reconcile the cited source records before response",
    ),
    (
        "PAYMENT_SHORTFALL",
        ("short payment", "fee due", "demand", "outstanding", "payment pending", "balance"),
        True,
        "reconcile and settle the outstanding amount",
    ),
    (
        "ELIGIBILITY",
        ("eligibility", "not eligible", "criteria", "qualification"),
        False,
        "prepare the eligibility evidence and route for authorised review",
    ),
    (
        "FORM_VALIDATION",
        ("invalid field", "validation error", "form error", "mandatory field", "invalid value"),
        True,
        "correct the affected form field",
    ),
    (
        "JURISDICTION",
        ("wrong office", "wrong authority", "jurisdiction", "transfer to", "competent authority"),
        False,
        "route the case to the competent authority without losing the case history",
    ),
    (
        "FIELD_VERIFICATION",
        ("site inspection", "physical verification", "field verification", "inspection required"),
        False,
        "schedule and prepare the authorised field verification",
    ),
    (
        "SYSTEM_ERROR",
        ("portal error", "technical issue", "system error", "timeout", "server", "not available"),
        False,
        "preserve the case packet and retry/replan the failed digital step",
    ),
]


def normalize_query(
    query: str | None,
    *,
    reference: str | None = None,
    task_id: str | None = None,
) -> Dict[str, Any]:
    raw = str(query or "").strip()
    lowered = raw.lower()
    for code, needles, applicant_fixable, action in QUERY_REASON_RULES:
        if any(needle in lowered for needle in needles):
            return {
                "code": code,
                "raw_query": raw,
                "reference": reference,
                "task_id": task_id,
                "applicant_fixable": applicant_fixable,
                "recommended_action": action,
                "confidence": 0.9,
            }

    return {
        "code": "OTHER_QUERY",
        "raw_query": raw,
        "reference": reference,
        "task_id": task_id,
        "applicant_fixable": False,
        "recommended_action": "assemble the relevant evidence and prepare an authorised response",
        "confidence": 0.55,
    }


def normalize_queries(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        normalize_query(
            item.get("query") or item.get("reason"),
            reference=item.get("reference"),
            task_id=item.get("task_id"),
        )
        for item in items
        if isinstance(item, dict)
    ]
