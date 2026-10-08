"""Cross-service journey cascades.

A cascade is a reusable map of likely downstream government work after a
milestone. Aether should only auto-create/submit downstream work when the exact
jurisdiction rule profile marks it as mandatory and the required authority and
connector scopes are present.
"""

JOURNEY_CASCADES = {
    "property_registration": [
        {"service_id": "mutation", "reason": "registered transaction may require land-record mutation"},
        {"service_id": "property_tax_assessment", "reason": "ownership/property record may affect municipal assessment"},
        {"service_id": "property_tax_payment", "reason": "new owner may need current tax record/payment"},
    ],
    "company_registration": [
        {"service_id": "gst_registration_update", "reason": "business may require tax registration/updates based on its activities"},
        {"service_id": "professional_tax_registration", "reason": "state tax registration may apply"},
        {"service_id": "shop_establishment_registration", "reason": "local establishment registration may apply"},
    ],
    "building_permit": [
        {"service_id": "building_completion_certificate", "reason": "completion action follows approved construction"},
        {"service_id": "occupancy_certificate", "reason": "occupancy permission may follow completion"},
        {"service_id": "property_tax_assessment", "reason": "built property may require assessment update"},
    ],
    "food_business_license": [
        {"service_id": "fire_noc", "reason": "fire-safety clearance may be required for the premises"},
        {"service_id": "sanitation_trade_clearance", "reason": "local health/sanitation clearance may apply"},
        {"service_id": "trade_license", "reason": "local trade licence may be required depending on jurisdiction"},
    ],
    "trade_license": [
        {"service_id": "food_business_license", "reason": "food-sector registration may apply to food businesses"},
        {"service_id": "fire_noc", "reason": "fire-safety clearance may apply based on premises/risk"},
    ],
}


def cascade_for(service_id: str) -> list[dict]:
    return [dict(item) for item in JOURNEY_CASCADES.get(service_id, [])]
