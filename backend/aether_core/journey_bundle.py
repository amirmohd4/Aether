from __future__ import annotations

from typing import Any, Dict, List

from .journey_cascades import cascade_for


SHARED_CASE_FIELDS = [
    "applicant_name",
    "owner_name",
    "company_name",
    "company_id",
    "property_id",
    "parcel_id",
    "project_id",
    "address",
    "pan",
    "gstin",
]


def build_journey_bundle(
    service_id: str,
    *,
    objective: str,
    inputs: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    candidates = cascade_for(service_id)
    return {
        "source_service_id": service_id,
        "objective": objective,
        "candidate_services": candidates,
        "shared_case_fields": SHARED_CASE_FIELDS,
        "shared_evidence_strategy": {
            "collect_once": True,
            "reuse_within_bundle": True,
            "future_reuse_requires_consent": True,
            "document_transfer_default": False,
        },
        "execution_policy": {
            "prepare_related_services": True,
            "auto_submit_without_jurisdiction_rule": False,
            "auto_submit_without_connector_scope": False,
            "ask_user_once_for_shared_information": True,
        },
        "user_experience": {
            "single_objective": objective,
            "show_related_services_as_one_journey": True,
            "show_only_additional_information": True,
            "avoid_duplicate_form_fields": True,
        },
        "input_fields_seen": sorted((inputs or {}).keys()),
    }
