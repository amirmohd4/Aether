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

    "factory_license": [
        {"service_id": "factory_plan_approval", "reason": "factory layout/plan approval may be required"},
        {"service_id": "pollution_consent", "reason": "environment consent may apply based on industry"},
        {"service_id": "fire_noc", "reason": "fire-safety clearance may apply based on premises/risk"},
    ],
    "hospital_empanelment": [
        {"service_id": "clinical_establishment_registration", "reason": "clinical establishment registration may be linked"},
        {"service_id": "drug_sale_license", "reason": "drug licence may apply where medicines are dispensed"},
    ],
    "vehicle_registration": [
        {"service_id": "vehicle_fitness_certificate", "reason": "fitness certification may apply to applicable vehicle classes"},
        {"service_id": "vehicle_permit", "reason": "transport permit may apply to commercial use"},
        {"service_id": "road_tax", "reason": "motor vehicle tax may be due"},
    ],
    "education_scholarship": [
        {"service_id": "education_scholarship", "reason": "scholarship verification/renewal continues through institute and nodal levels"},
    ],
    "passport": [
        {"service_id": "police_verification", "reason": "police verification may form part of the passport journey"},
        {"service_id": "character_certificate", "reason": "police certificate may be independently required for some purposes"},
    ],
    "land_mutation": [
        {"service_id": "property_tax_assessment", "reason": "updated ownership may affect local property records"},
        {"service_id": "property_tax_payment", "reason": "current tax dues may need reconciliation"},
    ],
}


def cascade_for(service_id: str) -> list[dict]:
    return [dict(item) for item in JOURNEY_CASCADES.get(service_id, [])]
