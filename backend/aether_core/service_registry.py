from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ServiceDefinition:
    id: str
    name: str
    department: str
    customer_types: List[str]
    keywords: List[str]
    template: Optional[str] = None
    outcome: str = "service_outcome"
    required_documents: List[str] | None = None
    human_authority_required: bool = True
    physical_action_possible: bool = False

    def documents(self) -> List[str]:
        return list(self.required_documents or [])


STOPWORDS = {"a", "an", "the", "to", "my", "i", "want", "need", "please", "me", "for", "this", "get", "apply", "application"}


def _normalize(value: str) -> str:
    import re
    tokens = re.findall(r"[a-z0-9]+(?:[-/][a-z0-9]+)*", value.lower())
    return " ".join(token for token in tokens if token not in STOPWORDS)

SERVICE_DEFINITIONS = [
    ("property_registration", "Property Registration", "Registration", ["citizen", "business", "bank", "developer", "insurer"], ["property registration", "register property"], "commercial_project", "registration_record"),
    ("mutation", "Land/Property Mutation", "Revenue", ["citizen", "business", "bank", "developer"], ["mutation", "transfer land record"], None, "updated_land_record"),
    ("encumbrance_certificate", "Encumbrance Certificate", "Registration", ["citizen", "business", "bank", "developer", "insurer"], ["encumbrance certificate", "ec"], "property_loan", "encumbrance_certificate"),
    ("land_conversion", "Land Conversion", "Revenue", ["citizen", "business", "developer"], ["land conversion", "convert land"], "commercial_project", "land_conversion_order"),
    ("title_verification", "Title Verification", "Revenue", ["bank", "insurer", "developer", "business"], ["title verification", "verify title", "property verification", "verify property", "bank loan", "property loan"], "property_loan", "title_evidence_package"),
    ("trade_license", "Trade License", "Municipal", ["citizen", "business", "developer"], ["trade license", "business license", "commercial license"], "restaurant", "trade_license"),
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
    ("company_registration", "Company Registration", "Corporate Registry", ["business"], ["company registration", "register company", "register a company", "incorporate company"], None, "company_registration"),
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
    ("food_business_license", "Food Business License/Registration", "Food Safety", ["citizen", "business", "developer"], ["restaurant", "cafe", "food business", "food license", "fssai"], "restaurant", "food_business_license"),
]


DEFAULT_DOCUMENTS = {
    "property": ["identity_document", "property_record"],
    "business": ["identity_document", "business_registration"],
    "building": ["identity_document", "site_plan", "building_plan"],
    "land": ["identity_document", "land_record"],
    "vehicle": ["identity_document", "vehicle_record"],
    "birth": ["identity_document", "birth_record"],
    "death": ["identity_document", "death_record"],
    "education": ["identity_document", "education_record"],
    "police": ["identity_document"],
    "passport": ["identity_document", "address_proof"],
    "visa": ["identity_document", "passport_document"],
    "housing": ["identity_document", "income_or_eligibility_proof"],
}


def _document_defaults(service_id: str) -> List[str]:
    if any(k in service_id for k in ("property", "mutation", "encumbrance", "land", "title", "registration")):
        return DEFAULT_DOCUMENTS["property"]
    if any(k in service_id for k in ("company", "gst", "factory", "trade", "medical", "pf_esi", "rera", "affordable")):
        return DEFAULT_DOCUMENTS["business"]
    if "building" in service_id:
        return DEFAULT_DOCUMENTS["building"]
    if "vehicle" in service_id:
        return DEFAULT_DOCUMENTS["vehicle"]
    if service_id == "birth_certificate":
        return DEFAULT_DOCUMENTS["birth"]
    if service_id == "death_certificate":
        return DEFAULT_DOCUMENTS["death"]
    if any(k in service_id for k in ("scholarship", "admission", "transfer")):
        return DEFAULT_DOCUMENTS["education"]
    if any(k in service_id for k in ("police", "fir")):
        return DEFAULT_DOCUMENTS["police"]
    if service_id == "passport":
        return DEFAULT_DOCUMENTS["passport"]
    if service_id == "visa":
        return DEFAULT_DOCUMENTS["visa"]
    if any(k in service_id for k in ("pmay", "housing", "subsidy", "ration")):
        return DEFAULT_DOCUMENTS["housing"]
    return ["identity_document"]


class ServiceRegistry:
    """Shared service identity and executable-process metadata for the MVP."""

    def __init__(self, definitions: List[tuple] = SERVICE_DEFINITIONS):
        self._services: Dict[str, ServiceDefinition] = {}
        for row in definitions:
            self._services[row[0]] = ServiceDefinition(
                id=row[0],
                name=row[1],
                department=row[2],
                customer_types=row[3],
                keywords=row[4],
                template=row[5],
                outcome=row[6],
                required_documents=_document_defaults(row[0]),
            )

    def get(self, service_id: str) -> Optional[ServiceDefinition]:
        return self._services.get(service_id)

    def all(self) -> List[ServiceDefinition]:
        return list(self._services.values())

    def resolve(self, objective: str, customer_type: str = "") -> Optional[ServiceDefinition]:
        service, _, _, _ = self.resolve_with_score(objective, customer_type)
        return service

    def resolve_with_score(
        self, objective: str, customer_type: str = ""
    ) -> Tuple[Optional[ServiceDefinition], int, List[str], int]:
        text = _normalize(objective)
        candidates = []
        for service in self._services.values():
            if customer_type and customer_type.lower() not in service.customer_types:
                continue
            matches = [
                keyword
                for keyword in service.keywords
                if _normalize(keyword) and _normalize(keyword) in text
            ]
            score = len(matches)
            if score:
                candidates.append((score, service, matches))
        candidates.sort(
            key=lambda item: (item[0], len(max(item[2], key=len, default=""))),
            reverse=True,
        )
        if not candidates:
            return None, 0, [], 0
        best = candidates[0]
        second_score = candidates[1][0] if len(candidates) > 1 else 0
        return best[1], best[0], best[2], best[0] - second_score

    def catalog(self) -> List[Dict[str, object]]:
        return [
            {
                "id": service.id,
                "name": service.name,
                "department": service.department,
                "customer_types": service.customer_types,
                "keywords": service.keywords,
                "template": service.template or "generic",
                "outcome": service.outcome,
                "required_documents": service.documents(),
            }
            for service in self.all()
        ]
