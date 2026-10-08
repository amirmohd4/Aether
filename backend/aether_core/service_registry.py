from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .india_service_catalog import INDIA_SERVICE_FAMILY_DEFINITIONS


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


STOPWORDS = {"a", "an", "the", "to", "my", "i", "want", "need", "please", "me", "for", "this", "get", "apply", "application", "service", "process"}

# Enterprise requests use the same service eligibility surface as business
# requests unless a service explicitly defines a different customer class.
CUSTOMER_TYPE_ALIASES = {
    "enterprise": "business",
}

SERVICE_ALIASES = {
    "property_registration": ["register a property", "property registry", "sale deed registration"],
    "mutation": ["mutation of property", "change land owner", "land record transfer", "record mutation"],
    "encumbrance_certificate": ["encumbrance", "property ec", "non encumbrance certificate"],
    "land_conversion": ["land use conversion", "agricultural to commercial land", "land diversion"],
    "title_verification": ["title check", "property title check", "real estate due diligence", "land verification"],
    "trade_license": ["municipal trade licence", "shop license", "business permit"],
    "building_permit": ["building approval", "construction permit", "building sanction"],
    "water_connection": ["new water connection", "water supply connection"],
    "birth_certificate": ["birth registration certificate", "register birth"],
    "death_certificate": ["death registration certificate", "register death"],
    "medical_license": ["doctor license", "clinic license", "medical establishment license"],
    "scholarship": ["student scholarship", "education scholarship"],
    "admission": ["school admission", "college admission", "education admission"],
    "transfer_certificate": ["school leaving certificate", "tc certificate"],
    "driving_license": ["driver license", "learner license", "driving licence"],
    "vehicle_registration": ["register vehicle", "rc registration", "motor vehicle registration"],
    "factory_license": ["factory licence", "factory approval", "industrial licence"],
    "pf_esi_registration": ["epf registration", "esic registration", "employee provident fund", "employees state insurance"],
    "gst_registration": ["register for gst", "goods and services tax registration", "gst number"],
    "company_registration": ["incorporate company", "company incorporation", "mca incorporation", "register private limited company"],
    "ration_card": ["food ration card", "public distribution ration card"],
    "pds_subsidy": ["food subsidy", "pds benefit"],
    "police_clearance": ["police clearance certificate", "pcc certificate"],
    "fir_report": ["file fir", "first information report"],
    "farmer_id": ["farmer registration", "farmer identity"],
    "crop_insurance": ["crop insurance claim", "farmer crop insurance"],
    "pmay": ["pradhan mantri awas yojana", "pmay housing benefit"],
    "affordable_housing": ["affordable housing project", "housing development project"],
    "rera_registration": ["real estate regulation registration", "register real estate project"],
    "court_case_filing": ["start a court case", "file a lawsuit", "legal case filing"],
    "e_court": ["e court services", "online court service"],
    "passport": ["new passport", "passport renewal"],
    "visa": ["visa application", "travel visa"],
    "food_business_license": ["food business registration", "restaurant license", "fssai registration", "cafe license"],
}

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

SERVICE_DEFINITIONS.extend(INDIA_SERVICE_FAMILY_DEFINITIONS)

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
    # Explicit service groups avoid substring collisions such as
    # company_registration/rera_registration inheriting property documents.
    property_services = {
        "property_registration",
        "mutation",
        "encumbrance_certificate",
        "land_conversion",
        "title_verification",
    }
    business_services = {
        "trade_license",
        "medical_license",
        "factory_license",
        "pf_esi_registration",
        "gst_registration",
        "company_registration",
        "rera_registration",
        "affordable_housing",
        "food_business_license",
    }

    if service_id in property_services:
        return DEFAULT_DOCUMENTS["property"]
    if service_id in business_services:
        return DEFAULT_DOCUMENTS["business"]
    if service_id == "building_permit":
        return DEFAULT_DOCUMENTS["building"]
    if service_id == "water_connection":
        return ["identity_document", "address_proof"]
    if service_id == "vehicle_registration":
        return DEFAULT_DOCUMENTS["vehicle"]
    if service_id == "driving_license":
        return ["identity_document", "address_proof"]
    if service_id == "birth_certificate":
        return DEFAULT_DOCUMENTS["birth"]
    if service_id == "death_certificate":
        return DEFAULT_DOCUMENTS["death"]
    if service_id in {"scholarship", "admission", "transfer_certificate"}:
        return DEFAULT_DOCUMENTS["education"]
    if service_id in {"police_clearance", "fir_report"}:
        return DEFAULT_DOCUMENTS["police"]
    if service_id == "passport":
        return DEFAULT_DOCUMENTS["passport"]
    if service_id == "visa":
        return DEFAULT_DOCUMENTS["visa"]
    if service_id in {"pmay", "ration_card", "pds_subsidy"}:
        return DEFAULT_DOCUMENTS["housing"]
    if service_id == "farmer_id":
        return ["identity_document", "land_record"]
    if service_id == "crop_insurance":
        return ["identity_document", "land_record", "crop_record"]
    if service_id == "court_case_filing":
        return ["identity_document", "case_documents"]
    if service_id == "e_court":
        return ["identity_document"]
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
                keywords=list(dict.fromkeys([*row[4], row[1], *SERVICE_ALIASES.get(row[0], [])])),
                template=row[5],
                outcome=row[6],
                required_documents=_document_defaults(row[0]),
                physical_action_possible=row[0] in {
                    "driving_license",
                    "vehicle_registration",
                    "medical_license",
                    "building_permit",
                    "factory_license",
                },
            )

    def get(self, service_id: str) -> Optional[ServiceDefinition]:
        return self._services.get(service_id)

    def all(self) -> List[ServiceDefinition]:
        return list(self._services.values())

    def resolve(self, objective: str, customer_type: str = "") -> Optional[ServiceDefinition]:
        service, _, _, _ = self.resolve_with_score(objective, customer_type)
        return service

    def _rank_candidates(self, objective: str, customer_type: str = ""):
        text = _normalize(objective)
        tokens = set(text.split())
        candidates = []
        requested_customer_type = CUSTOMER_TYPE_ALIASES.get(
            customer_type.strip().lower(),
            customer_type.strip().lower(),
        )
        for service in self._services.values():
            if requested_customer_type and requested_customer_type not in service.customer_types:
                continue
            matches: List[str] = []
            score = 0
            for keyword in service.keywords:
                normalized = _normalize(keyword)
                if not normalized:
                    continue
                if normalized in text:
                    weight = 6 if len(normalized.split()) >= 2 else 4
                    score = max(score, weight)
                    matches.append(keyword)
                    continue
                keyword_tokens = set(normalized.split())
                overlap = len(tokens & keyword_tokens)
                if overlap and overlap >= max(1, len(keyword_tokens) // 2):
                    score += overlap
                    matches.append(keyword)
            if service.id and _normalize(service.name) in text:
                score += 3
            if score:
                candidates.append((score, service, sorted(set(matches))))
        candidates.sort(key=lambda item: (item[0], len(max(item[2], key=len, default=""))), reverse=True)
        return candidates

    def resolve_with_score(
        self, objective: str, customer_type: str = ""
    ) -> Tuple[Optional[ServiceDefinition], int, List[str], int]:
        candidates = self._rank_candidates(objective, customer_type)
        if not candidates:
            return None, 0, [], 0
        best = candidates[0]
        second_score = candidates[1][0] if len(candidates) > 1 else 0
        return best[1], best[0], best[2], best[0] - second_score

    def candidates(
        self, objective: str, customer_type: str = "", limit: int = 5
    ) -> List[Dict[str, object]]:
        return [
            {
                "service_id": service.id,
                "service_name": service.name,
                "department": service.department,
                "score": score,
                "matched_keywords": matches,
            }
            for score, service, matches in self._rank_candidates(objective, customer_type)[:limit]
        ]

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
