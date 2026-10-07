from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ServiceDefinition:
    id: str
    name: str
    department: str
    customer_types: List[str]
    keywords: List[str]
    template: Optional[str] = None
    outcome: str = "service_outcome"


SERVICE_DEFINITIONS = [
    ("property_registration", "Property Registration", "Registration", ["citizen", "business", "bank", "developer", "insurer"], ["property registration", "register property"], "commercial_project", "registration_record"),
    ("mutation", "Land/Property Mutation", "Revenue", ["citizen", "business", "bank", "developer"], ["mutation", "transfer land record"], None, "updated_land_record"),
    ("encumbrance_certificate", "Encumbrance Certificate", "Registration", ["citizen", "business", "bank", "developer", "insurer"], ["encumbrance certificate", "ec"], "property_loan", "encumbrance_certificate"),
    ("land_conversion", "Land Conversion", "Revenue", ["citizen", "business", "developer"], ["land conversion", "convert land"], "commercial_project", "land_conversion_order"),
    ("title_verification", "Title Verification", "Revenue", ["bank", "insurer", "developer", "business"], ["title verification", "verify title"], "property_loan", "title_evidence_package"),
    ("trade_license", "Trade License", "Municipal", ["citizen", "business"], ["trade license", "business license"], "restaurant", "trade_license"),
    ("building_permit", "Building Permit", "Municipal", ["citizen", "business", "developer"], ["building permit", "building permission"], "commercial_project", "building_permission"),
    ("water_connection", "Water Connection", "Municipal", ["citizen", "business"], ["water connection"], None, "water_connection"),
    ("birth_certificate", "Birth Certificate", "Health", ["citizen"], ["birth certificate"], None, "birth_certificate"),
    ("death_certificate", "Death Certificate", "Health", ["citizen"], ["death certificate"], None, "death_certificate"),
    ("medical_license", "Medical License", "Health", ["business"], ["medical license", "medical licence"], None, "medical_license"),
    ("scholarship", "Scholarship", "Education", ["citizen"], ["scholarship"], None, "scholarship_decision"),
    ("admission", "Education Admission", "Education", ["citizen"], ["admission", "school admission"], None, "admission_decision"),
    ("transfer_certificate", "Transfer Certificate", "Education", ["citizen"], ["transfer certificate"], None, "transfer_certificate"),
    ("driving_license", "Driving License", "Transport", ["citizen"], ["driving license", "driving licence"], None, "driving_license"),
    ("vehicle_registration", "Vehicle Registration", "Transport", ["citizen", "business"], ["vehicle registration"], None, "vehicle_registration"),
    ("factory_license", "Factory License", "Labour", ["business", "developer"], ["factory license", "factory licence"], "commercial_project", "factory_license"),
    ("pf_esi_registration", "PF/ESI Registration", "Labour", ["business"], ["pf registration", "esi registration", "pf/esi"], None, "labour_registration"),
    ("gst_registration", "GST Registration", "Tax", ["business"], ["gst registration"], None, "gst_registration"),
    ("company_registration", "Company Registration", "Corporate Registry", ["business"], ["company registration", "register company"], None, "company_registration"),
    ("ration_card", "Ration Card", "Food & Civil Supplies", ["citizen"], ["ration card"], None, "ration_card"),
    ("pds_subsidy", "PDS Subsidy", "Food & Civil Supplies", ["citizen"], ["pds subsidy", "food subsidy"], None, "subsidy_decision"),
    ("police_clearance", "Police Clearance", "Police", ["citizen", "business"], ["police clearance", "pcc"], None, "police_clearance"),
    ("fir_report", "FIR Report", "Police", ["citizen", "business"], ["fir report"], None, "fir_report"),
    ("farmer_id", "Farmer ID", "Agriculture", ["citizen", "business"], ["farmer id", "farmer identity"], None, "farmer_id"),
    ("crop_insurance", "Crop Insurance", "Agriculture", ["citizen", "insurer"], ["crop insurance"], None, "crop_insurance"),
    ("pmay", "PMAY Housing", "Housing", ["citizen"], ["pmay", "housing assistance"], None, "housing_benefit"),
    ("affordable_housing", "Affordable Housing", "Housing", ["citizen", "developer"], ["affordable housing"], "commercial_project", "housing_project"),
    ("rera_registration", "RERA Project Registration", "RERA", ["developer", "business"], ["rera registration", "rera"], "commercial_project", "rera_registration"),
    ("court_case_filing", "Court Case Filing", "Courts", ["citizen", "business"], ["court case filing", "file court case"], None, "case_filing"),
    ("e_court", "E-Court Service", "Courts", ["citizen", "business"], ["e-court", "ecourt"], None, "court_service"),
    ("passport", "Passport Application", "Passport", ["citizen"], ["passport application", "passport"], None, "passport"),
    ("visa", "Visa Service", "Passport", ["citizen", "business"], ["visa service", "visa application"], None, "visa_service"),
    ("food_business_license", "Food Business License/Registration", "Food Safety", ["citizen", "business"], ["restaurant", "cafe", "food business", "food license", "fssai"], "restaurant", "food_business_license"),
]


class ServiceRegistry:
    """Shared service identity layer for Aether's GovOS execution graph."""

    def __init__(self, definitions: List[tuple] = SERVICE_DEFINITIONS):
        self._services: Dict[str, ServiceDefinition] = {
            row[0]: ServiceDefinition(
                id=row[0], name=row[1], department=row[2], customer_types=row[3],
                keywords=row[4], template=row[5], outcome=row[6],
            )
            for row in definitions
        }

    def get(self, service_id: str) -> Optional[ServiceDefinition]:
        return self._services.get(service_id)

    def all(self) -> List[ServiceDefinition]:
        return list(self._services.values())

    def resolve(self, objective: str, customer_type: str = "") -> Optional[ServiceDefinition]:
        text = f"{objective} {customer_type}".lower()
        candidates = []
        for service in self._services.values():
            if service.customer_types and customer_type.lower() not in service.customer_types:
                continue
            score = sum(1 for keyword in service.keywords if keyword in text)
            if score:
                candidates.append((score, service))
        return max(candidates, key=lambda item: item[0])[1] if candidates else None
