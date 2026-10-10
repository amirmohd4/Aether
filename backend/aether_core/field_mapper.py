from __future__ import annotations

from typing import Any, Dict, Iterable


DEFAULT_FIELD_ALIASES: Dict[str, tuple[str, ...]] = {
    "applicant_name": ("applicantName", "name_of_applicant", "applicant_name"),
    "owner_name": ("ownerName", "property_owner_name", "owner_name"),
    "company_name": ("companyName", "legal_name", "company_name"),
    "company_id": ("companyId", "cin", "entity_id", "company_id"),
    "property_id": ("propertyId", "property_uid", "property_id"),
    "parcel_id": ("parcelId", "survey_number", "khasra_no", "parcel_id"),
    "project_id": ("projectId", "project_number", "project_id"),
    "address": ("address", "registered_address", "communication_address"),
    "pan": ("pan", "pan_no", "permanent_account_number"),
    "gstin": ("gstin", "gst_number", "gstin_no"),
    "tax_id": ("taxId", "taxpayer_id", "tax_account_number"),
    "registration_id": ("registrationId", "registration_number", "registration_id"),
    "certificate_reference": ("certificateReference", "certificate_number", "certificate_reference"),
    "record_reference": ("recordReference", "record_number", "record_reference"),
}


def prepare_form_mapping(
    fields: Dict[str, Any],
    provenance: Dict[str, Dict[str, Any]] | None = None,
    target_field_map: Dict[str, str] | None = None,
    required_fields: Iterable[str] | None = None,
) -> Dict[str, Any]:
    provenance = provenance or {}
    target_field_map = target_field_map or {}
    required = {str(field) for field in (required_fields or [])}

    mapped = []
    unmapped = []
    for canonical, value in sorted(fields.items()):
        target = target_field_map.get(canonical)
        if not target:
            target = DEFAULT_FIELD_ALIASES.get(canonical, (canonical,))[0]

        mapped.append({
            "canonical_field": canonical,
            "target_field": target,
            "value": value,
            "provenance": provenance.get(canonical),
            "verified": bool(provenance.get(canonical)),
        })

    for field in sorted(required):
        if field not in fields:
            unmapped.append({
                "canonical_field": field,
                "target_field": target_field_map.get(field) or DEFAULT_FIELD_ALIASES.get(field, (field,))[0],
            })

    return {
        "mapped_fields": mapped,
        "unmapped_required_fields": unmapped,
        "mapping_status": "ready" if not unmapped else "needs_fields",
        "copy_paste_eliminated": True,
        "manual_reentry_remaining": len(unmapped),
    }
