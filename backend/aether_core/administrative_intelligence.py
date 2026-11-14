"""India-wide administrative intelligence layer for Aether.

The seed taxonomy is an operational discovery aid, not a statutory service
catalogue. Jurisdiction-specific requirements and dependency edges must be
backed by effective-dated official sources before live execution.
"""
from __future__ import annotations

from typing import Any
import re

from .service_registry import ServiceRegistry


DEPARTMENT_PROFILES: list[dict[str, Any]] = [
    {"id": "revenue", "name": "Revenue & Land Administration", "aliases": ["revenue", "land records"], "levels": ["state", "district", "subdistrict"], "domains": ["land_records", "certificates", "mutation", "demarcation", "land_use"], "examples": ["Jamabandi / Record of Rights", "Mutation", "Domicile and income certificates", "Land demarcation"], "coordination_partners": ["registration_stamps", "urban_local_government", "development_authority", "courts"]},
    {"id": "urban_local_government", "name": "Urban Local Government", "aliases": ["municipal", "municipality", "urban local body", "ulb"], "levels": ["state", "city", "municipal"], "domains": ["building_permissions", "trade_licences", "property_tax", "water_sewer", "occupancy"], "examples": ["Building permission", "Trade licence", "Property tax", "Occupancy / completion certificate"], "coordination_partners": ["revenue", "fire_services", "water_resources", "electricity", "pollution_control"]},
    {"id": "development_authority", "name": "Development & Planning Authorities", "aliases": ["development authority", "town planning", "planning authority"], "levels": ["state", "regional", "city"], "domains": ["master_planning", "zoning", "layout_approval", "land_use"], "examples": ["Land-use / zoning review", "Layout approval", "Development permission"], "coordination_partners": ["revenue", "urban_local_government", "environment", "fire_services"]},
    {"id": "registration_stamps", "name": "Registration & Stamps", "aliases": ["registration", "registrar", "stamps"], "levels": ["state", "district", "subdistrict"], "domains": ["deed_registration", "stamp_duty", "encumbrance", "certified_copies"], "examples": ["Sale deed registration", "Lease registration", "Encumbrance search", "Certified deed copy"], "coordination_partners": ["revenue", "taxation", "banks"]},
    {"id": "industries_commerce", "name": "Industries & Commerce", "aliases": ["industries", "industry", "commerce", "single window"], "levels": ["central", "state", "district"], "domains": ["industrial_approvals", "incentives", "enterprise_facilitation"], "examples": ["Industrial project approvals", "Incentive applications", "Single-window facilitation"], "coordination_partners": ["labour", "pollution_control", "fire_services", "power", "water_resources"]},
    {"id": "labour", "name": "Labour & Employment", "aliases": ["labour", "labor", "employment"], "levels": ["central", "state", "district"], "domains": ["establishment_registration", "factory_licences", "worker_compliance"], "examples": ["Shops and Establishments", "Factory licence", "Contract labour licence", "Employment services"], "coordination_partners": ["industries_commerce", "taxation", "social_security"]},
    {"id": "health", "name": "Health & Medical Establishments", "aliases": ["health", "medical", "health services"], "levels": ["central", "state", "district"], "domains": ["clinical_establishments", "drug_control", "health_certificates"], "examples": ["Clinical establishment registration", "Drug sale licence", "Health certificates"], "coordination_partners": ["urban_local_government", "fire_services", "pollution_control"]},
    {"id": "food_safety", "name": "Food Safety & Standards", "aliases": ["food safety", "fssai", "food standards"], "levels": ["central", "state", "district"], "domains": ["food_business_registration", "food_safety_compliance"], "examples": ["Food business registration / licence", "Food safety compliance"], "coordination_partners": ["urban_local_government", "health", "labour"]},
    {"id": "fire_services", "name": "Fire & Emergency Services", "aliases": ["fire", "fire and emergency", "fire services"], "levels": ["state", "district", "city"], "domains": ["fire_noc", "inspection", "emergency_response"], "examples": ["Fire safety NOC", "Fire inspection", "Renewal / compliance"], "coordination_partners": ["urban_local_government", "development_authority", "industries_commerce", "tourism"]},
    {"id": "pollution_control", "name": "Environment & Pollution Control", "aliases": ["environment", "pollution", "pollution control", "pcb", "spcb"], "levels": ["central", "state", "regional"], "domains": ["consent_to_establish", "consent_to_operate", "environmental_clearance", "waste_authorisation"], "examples": ["Consent to Establish", "Consent to Operate", "Environmental clearance", "Waste authorisation"], "coordination_partners": ["industries_commerce", "urban_local_government", "forest"]},
    {"id": "forest", "name": "Forest, Wildlife & Ecology", "aliases": ["forest", "wildlife", "ecology"], "levels": ["central", "state", "division"], "domains": ["forest_clearance", "wildlife_clearance", "tree_permissions"], "examples": ["Forest diversion proposals", "Wildlife permissions", "Tree felling permissions"], "coordination_partners": ["environment", "revenue", "development_authority"]},
    {"id": "tourism", "name": "Tourism", "aliases": ["tourism", "tourist"], "levels": ["central", "state", "district"], "domains": ["tourism_registration", "accommodation", "tour_operator"], "examples": ["Accommodation registration", "Tour operator registration", "Tourism incentives"], "coordination_partners": ["urban_local_government", "fire_services", "food_safety", "labour"]},
    {"id": "transport", "name": "Transport & Road Safety", "aliases": ["transport", "rto", "motor vehicles"], "levels": ["central", "state", "district"], "domains": ["driving_licences", "vehicle_registration", "permits", "fitness"], "examples": ["Driving licence", "Vehicle registration", "Commercial permits", "Fitness certificate"], "coordination_partners": ["police", "taxation"]},
    {"id": "agriculture", "name": "Agriculture", "aliases": ["agriculture", "agri"], "levels": ["central", "state", "district", "block"], "domains": ["farmer_registration", "subsidies", "crop_insurance", "input_licences"], "examples": ["Farmer registration", "Agricultural schemes", "Crop insurance facilitation"], "coordination_partners": ["revenue", "banking", "insurance"]},
    {"id": "horticulture", "name": "Horticulture", "aliases": ["horticulture"], "levels": ["central", "state", "district"], "domains": ["orchard_support", "plantation_schemes", "post_harvest"], "examples": ["Orchard development schemes", "Plantation support", "Post-harvest assistance"], "coordination_partners": ["agriculture", "revenue", "banking"]},
    {"id": "education", "name": "School & Higher Education", "aliases": ["education", "school", "higher education"], "levels": ["central", "state", "district", "institution"], "domains": ["admissions", "scholarships", "certificates", "institution_recognition"], "examples": ["Scholarships", "Admissions", "Transfer certificates", "Institution recognition"], "coordination_partners": ["social_welfare", "revenue", "banking"]},
    {"id": "social_welfare", "name": "Social Welfare & Empowerment", "aliases": ["social welfare", "social justice", "empowerment"], "levels": ["central", "state", "district"], "domains": ["pensions", "disability", "welfare_schemes", "beneficiary_verification"], "examples": ["Pensions", "Disability-related services", "Welfare scheme applications"], "coordination_partners": ["health", "revenue", "banking"]},
    {"id": "rural_development", "name": "Rural Development & Panchayati Raj", "aliases": ["rural development", "panchayati raj", "panchayat"], "levels": ["central", "state", "district", "block", "panchayat"], "domains": ["rural_works", "panchayat_services", "rural_housing", "scheme_delivery"], "examples": ["Rural works", "Panchayat certificates / services", "Rural housing schemes"], "coordination_partners": ["revenue", "water_resources", "power", "social_welfare"]},
    {"id": "water_resources", "name": "Jal Shakti, Water & Sewerage", "aliases": ["jal shakti", "water", "water resources", "sewerage", "phed"], "levels": ["central", "state", "district", "utility"], "domains": ["water_connections", "sewerage", "bulk_supply", "water_clearances"], "examples": ["Water connection", "Sewer connection", "Bulk water supply"], "coordination_partners": ["urban_local_government", "industries_commerce", "rural_development"]},
    {"id": "power", "name": "Power & Electricity Utilities", "aliases": ["power", "electricity", "energy", "discom"], "levels": ["central", "state", "district", "utility"], "domains": ["new_connections", "load_sanction", "metering", "utility_clearances"], "examples": ["New electricity connection", "Load enhancement", "Meter services"], "coordination_partners": ["urban_local_government", "industries_commerce", "water_resources"]},
    {"id": "taxation", "name": "Taxation & Revenue Authorities", "aliases": ["tax", "taxation", "gst", "income tax"], "levels": ["central", "state", "district"], "domains": ["tax_registration", "returns", "assessments", "refunds"], "examples": ["GST registration", "Tax returns", "Tax notices and refunds"], "coordination_partners": ["registration_stamps", "industries_commerce", "labour"]},
    {"id": "police", "name": "Police & Public Safety", "aliases": ["police", "home department", "public safety"], "levels": ["central", "state", "district", "station"], "domains": ["clearance_certificates", "verification", "public_grievances"], "examples": ["Police clearance", "Character verification", "Public safety services"], "coordination_partners": ["transport", "district_administration"]},
    {"id": "civil_supplies", "name": "Food, Civil Supplies & Consumer Affairs", "aliases": ["food and civil supplies", "civil supplies", "consumer affairs", "pds"], "levels": ["central", "state", "district"], "domains": ["ration_cards", "pds", "consumer_services"], "examples": ["Ration card", "Public Distribution System", "Consumer services"], "coordination_partners": ["revenue", "social_welfare"]},
    {"id": "district_administration", "name": "District Administration & General Administration", "aliases": ["district administration", "general administration", "dc office", "deputy commissioner"], "levels": ["central", "state", "district"], "domains": ["public_service_delivery", "certificates", "coordination", "grievances"], "examples": ["District-level certificates", "Public grievance coordination", "Inter-department escalation"], "coordination_partners": ["revenue", "police", "social_welfare", "rural_development"]},
    {"id": "courts", "name": "Courts & Justice Administration", "aliases": ["court", "courts", "justice", "judiciary"], "levels": ["central", "state", "district"], "domains": ["case_information", "filing_support", "orders_and_certified_copies"], "examples": ["Case status", "Filing support", "Certified copies"], "coordination_partners": ["police", "revenue", "registration_stamps"]},
]


# Journey edges are planning relationships, not assertions of mandatory legal
# prerequisites. Conditions and legal basis must be verified for each location.
JOURNEY_TEMPLATES: list[dict[str, Any]] = [
    {
        "id": "establish_hotel",
        "name": "Establish and operate a hotel",
        "description": "Coordinate land, planning, building, safety, utilities and operating permissions for a hotel project.",
        "customer_types": ["business", "developer"],
        "steps": [
            {"id": "land_evidence", "service_id": "title_verification", "label": "Assemble land and title evidence", "condition": "where land ownership or control must be established"},
            {"id": "land_use", "service_id": "land_conversion", "label": "Check land-use position and conversion route", "condition": "only if the existing land use does not permit the proposed activity"},
            {"id": "building", "service_id": "building_permit", "label": "Prepare and track building permission", "condition": "where construction or building alteration requires permission"},
            {"id": "fire", "service_id": "fire_noc", "label": "Coordinate applicable fire-safety scrutiny", "condition": "as required by building type, height, occupancy and local rules"},
            {"id": "environment", "service_id": "pollution_consent", "label": "Check pollution-control applicability", "condition": "only where activity and thresholds trigger consent"},
            {"id": "water", "service_id": "water_connection", "label": "Coordinate water connection", "condition": "where a new or modified connection is needed"},
            {"id": "food", "service_id": "food_business_license", "label": "Check food-business licensing", "condition": "if the hotel operates a restaurant or food service"},
            {"id": "trade", "service_id": "trade_license", "label": "Check local trade / establishment permission", "condition": "subject to local body rules and applicable exemptions"},
        ],
        "edges": [["land_evidence", "land_use", "conditional"], ["land_use", "building", "planning_dependency"], ["building", "fire", "conditional"], ["building", "environment", "conditional"], ["building", "water", "operational_dependency"], ["building", "food", "conditional"], ["building", "trade", "conditional"]],
    },
    {
        "id": "set_up_manufacturing_unit",
        "name": "Set up a manufacturing unit",
        "description": "Coordinate entity, land, factory, environment, worker-safety and utility workstreams.",
        "customer_types": ["business", "developer"],
        "steps": [
            {"id": "entity", "service_id": "company_registration", "label": "Establish or verify the legal entity", "condition": "if a new company is being incorporated"},
            {"id": "land", "service_id": "title_verification", "label": "Assemble site and title evidence", "condition": "where site control or ownership evidence is required"},
            {"id": "land_use", "service_id": "land_conversion", "label": "Check industrial land-use eligibility", "condition": "if existing land use does not permit the proposed activity"},
            {"id": "factory_plan", "service_id": "factory_plan_approval", "label": "Check factory plan approval applicability", "condition": "as prescribed for the factory and jurisdiction"},
            {"id": "pollution", "service_id": "pollution_consent", "label": "Determine Consent to Establish / Operate route", "condition": "based on category, process and applicable thresholds"},
            {"id": "environment", "service_id": "environmental_clearance", "label": "Screen environmental clearance applicability", "condition": "only if project category / thresholds trigger it"},
            {"id": "factory", "service_id": "factory_license", "label": "Coordinate factory licence", "condition": "where the Factories Act / applicable successor framework and state rules require it"},
            {"id": "power", "service_id": "electricity_connection", "label": "Coordinate power connection and load", "condition": "based on sanctioned load and utility rules"},
            {"id": "water", "service_id": "water_connection", "label": "Coordinate industrial water supply", "condition": "where required by process and utility rules"},
        ],
        "edges": [["entity", "land", "planning_dependency"], ["land", "land_use", "conditional"], ["land_use", "factory_plan", "planning_dependency"], ["factory_plan", "factory", "planning_dependency"], ["factory_plan", "pollution", "conditional"], ["pollution", "environment", "conditional"], ["factory_plan", "power", "operational_dependency"], ["factory_plan", "water", "operational_dependency"]],
    },
    {
        "id": "develop_real_estate_project",
        "name": "Develop a real-estate project",
        "description": "Coordinate land evidence, planning, project registration, building permissions and completion-stage records.",
        "customer_types": ["developer", "business"],
        "steps": [
            {"id": "title", "service_id": "title_verification", "label": "Assemble title and land evidence", "condition": "for site due diligence"},
            {"id": "land_use", "service_id": "land_conversion", "label": "Check land-use route", "condition": "if the proposed use is not already permitted"},
            {"id": "rera", "service_id": "rera_registration", "label": "Screen RERA project registration", "condition": "subject to project type, size, exemptions and applicable RERA rules"},
            {"id": "building", "service_id": "building_permit", "label": "Coordinate building plan permission", "condition": "as required by local planning law"},
            {"id": "fire", "service_id": "fire_noc", "label": "Coordinate applicable fire approval", "condition": "as required by building classification and local rules"},
            {"id": "pollution", "service_id": "pollution_consent", "label": "Screen pollution-control requirements", "condition": "only if project activity triggers consent"},
        ],
        "edges": [["title", "land_use", "conditional"], ["land_use", "rera", "planning_dependency"], ["land_use", "building", "planning_dependency"], ["building", "fire", "conditional"], ["building", "pollution", "conditional"]],
    },
]


class AdministrativeIntelligence:
    """Read-only administrative map assembled from Aether's service registry."""

    def __init__(self, registry: ServiceRegistry | None = None) -> None:
        self.registry = registry or ServiceRegistry(include_extended=True)
        self.services = self.registry.all()
        self.by_id = {service.id: service for service in self.services}

    @staticmethod
    def _matches(profile: dict[str, Any], department: str) -> bool:
        def normalize(value: str) -> str:
            return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

        value = normalize(department)
        if not value:
            return False
        padded_value = f" {value} "
        for alias in profile["aliases"]:
            normalized_alias = normalize(alias)
            if normalized_alias and f" {normalized_alias} " in padded_value:
                return True
        return False

    def departments(self) -> list[dict[str, Any]]:
        result = []
        for profile in DEPARTMENT_PROFILES:
            services = [s for s in self.services if self._matches(profile, s.department)]
            result.append({
                **profile,
                "service_count": len(services),
                "services": [{"id": s.id, "name": s.name, "department_label": s.department, "customer_types": s.customer_types} for s in services],
                "catalog_status": "seeded_service_matches",
                "legal_completeness": "not_assessed",
                "jurisdiction_coverage": "national_family_seed_only",
            })
        return result

    def journeys(self) -> list[dict[str, Any]]:
        result = []
        for journey in JOURNEY_TEMPLATES:
            steps = []
            included = set()
            for step in journey["steps"]:
                service = self.by_id.get(step["service_id"])
                if not service:
                    continue
                included.add(step["id"])
                steps.append({**step, "service_name": service.name, "department": service.department})
            edges = [
                {"from": source, "to": target, "relationship": relationship,
                 "legal_basis_status": "not_verified", "is_statutory_prerequisite": None}
                for source, target, relationship in journey["edges"]
                if source in included and target in included
            ]
            result.append({
                "id": journey["id"], "name": journey["name"],
                "description": journey["description"], "customer_types": journey["customer_types"],
                "steps": steps, "edges": edges,
                "status": "illustrative_planning_template",
                "warning": "This graph is not a legal checklist. Actual applicability, sequence and statutory prerequisites must be verified for the selected State/UT, district, project facts and effective-dated official rules.",
            })
        return result

    def overview(self) -> dict[str, Any]:
        departments = self.departments()
        return {
            "product": "Aether India Administrative Intelligence",
            "catalog_scope": "India-wide service-family seed; jurisdiction-specific validation required",
            "service_registry_count": len(self.services),
            "department_profiles": len(departments),
            "departments_with_seeded_service_matches": sum(1 for d in departments if d["service_count"]),
            "journey_templates": len(JOURNEY_TEMPLATES),
            "live_government_execution_enabled": False,
            "source_of_truth": "The relevant government department / statutory authority remains the system of record.",
            "next_required_data": ["official service URL", "controlling Act/Rule/notification", "jurisdiction", "effective date", "eligibility", "documents", "notified timeline", "designated authority", "submission channel", "integration authorization"],
        }
