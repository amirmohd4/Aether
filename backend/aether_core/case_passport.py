from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Any, Dict


def build_case_passport(
    case_id: str,
    service_id: str | None,
    jurisdiction: Dict[str, Any],
    task_results: Dict[str, Any],
    verified_fields: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    evidence = []
    for task_id, result in sorted(task_results.items()):
        if not isinstance(result, dict):
            continue
        ref = (
            result.get("reference")
            or result.get("record_reference")
            or result.get("certificate_reference")
            or result.get("registration_id")
        )
        if ref:
            evidence.append({
                "task_id": task_id,
                "reference": ref,
                "source": result.get("source"),
            })

    packet = {
        "version": "1",
        "case_id": case_id,
        "service_id": service_id,
        "jurisdiction": jurisdiction,
        "verified_fields": dict(verified_fields or {}),
        "evidence_references": evidence,
        "documents_included": False,
        "sharing_note": "Portable administrative handoff packet; authoritative receiving systems and officers determine acceptance and legal effect.",
    }
    canonical = json.dumps(packet, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    secret = os.getenv("AETHER_CASE_PASSPORT_SECRET", "").encode("utf-8")
    signature = hmac.new(secret, canonical, hashlib.sha256).hexdigest() if secret else None

    return {
        **packet,
        "integrity": {
            "sha256": digest,
            "hmac_sha256": signature,
            "signed": bool(signature),
        },
    }
