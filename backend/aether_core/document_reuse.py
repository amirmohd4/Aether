from __future__ import annotations

from typing import Any, Dict, List


def build_document_reuse_candidates(
    store,
    *,
    sha256: str,
    tenant_id: str | None,
    owner_user_id: str | None,
    current_case_id: str | None = None,
) -> Dict[str, Any]:
    if not sha256:
        return {
            "status": "unavailable",
            "candidates": [],
            "policy": {
                "auto_transfer": False,
                "explicit_confirmation_required": True,
            },
        }

    rows = store.documents_by_hash(
        sha256,
        tenant_id=tenant_id,
        owner_user_id=owner_user_id,
    )
    candidates = [
        item for item in rows
        if item.get("case_id") != current_case_id
    ]

    return {
        "status": "found" if candidates else "none",
        "match_type": "exact_sha256",
        "candidates": candidates,
        "policy": {
            "auto_transfer": False,
            "explicit_confirmation_required": True,
            "scope": "same_authenticated_owner_and_tenant",
            "document_bytes_not_copied_by_this_planner": True,
        },
    }
