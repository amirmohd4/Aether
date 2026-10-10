from __future__ import annotations

from typing import Any, Dict, List


def simulate_submission(
    *,
    service: Any,
    requirements: List[Any],
    inputs: Dict[str, Any],
    process_profile: Dict[str, Any] | None = None,
    journey_playbook: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    submitted = {
        str(item.get("type")) if isinstance(item, dict) else str(item)
        for item in (inputs.get("documents") or [])
    }
    required_documents: List[str] = []
    for requirement in requirements or []:
        if isinstance(requirement, dict):
            required_documents.extend(str(doc) for doc in requirement.get("documents", []))
        else:
            required_documents.extend(str(doc) for doc in getattr(requirement, "documents", []) or [])
    required_documents = sorted(set(required_documents))
    missing = [doc for doc in required_documents if doc not in submitted]

    blockers = [{"code": "MISSING_DOCUMENT", "document_type": doc} for doc in missing]
    warnings: List[Dict[str, Any]] = []

    # Prevent avoidable duplicate filing where the user already has a stable
    # registration/identifier in their supplied inputs.
    service_id = getattr(service, "id", None)
    existing_identifiers = [
        key for key in ("registration_id", "certificate_reference", "gstin", "udyam_registration")
        if inputs.get(key)
    ]
    if existing_identifiers:
        warnings.append({
            "code": "EXISTING_IDENTIFIER",
            "fields": existing_identifiers,
            "message": "An existing authoritative identifier was supplied; Aether should check for amendment/renewal instead of creating a duplicate case where rules permit.",
        })

    # Internal consistency check catches obvious mismatches before submission.
    consistency_pairs = [
        ("owner_name", "applicant_name"),
        ("company_name", "registered_company_name"),
    ]
    for left, right in consistency_pairs:
        if inputs.get(left) and inputs.get(right) and str(inputs[left]).strip() != str(inputs[right]).strip():
            blockers.append({
                "code": "INPUT_MISMATCH",
                "fields": [left, right],
                "message": "Resolve the conflicting values before submission.",
            })

    profile_status = str((process_profile or {}).get("status") or "missing")
    if profile_status != "ready":
        warnings.append({
            "code": "JURISDICTION_PROFILE_NOT_READY",
            "status": profile_status,
            "message": "Aether can prepare the case, but production submission must wait for a verified jurisdiction-specific process profile.",
        })

    playbook = journey_playbook or {}
    human_boundaries = list(playbook.get("human_boundary") or [])
    parallel = list(playbook.get("parallelizable") or [])

    return {
        "service_id": service_id,
        "status": "fix_before_submit" if blockers else "ready_to_prepare" if profile_status != "ready" else "ready",
        "readiness": {
            "blocker_count": len(blockers),
            "warning_count": len(warnings),
            "required_document_count": len(required_documents),
            "submitted_document_count": len(submitted),
            "human_boundary_count": len(human_boundaries),
            "parallel_workstreams": parallel,
        },
        "blockers": blockers[:25],
        "warnings": warnings[:25],
        "next_steps": [
            "Resolve blockers shown above.",
            "Aether will build one case packet and reuse verified facts within the authorised journey.",
            "Only statutory, field or explicitly authorised actions remain with the responsible authority.",
        ],
        "journey_preview": {
            "stages": list(playbook.get("stages") or []),
            "citizen_wait_points": list(playbook.get("citizen_wait_points") or []),
            "human_boundary": human_boundaries,
        },
        "policy": {
            "no_external_submission_performed": True,
            "no_statutory_decision_made": True,
        },
    }
