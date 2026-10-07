from typing import Dict, List

from .domain import TaskDefinition


def _jk(source: str, title: str, reason: str, documents: List[str]) -> Dict:
    return {
        "states": ["Jammu and Kashmir"],
        "source": source,
        "source_title": title,
        "verified_at": "2026-10-07",
        "confidence": "source-backed-mvp",
        "reason": reason,
        "documents": documents,
    }


def restaurant_requirements() -> List[Dict]:
    return [
        {"id": "identity", "name": "Identity verification", "documents": ["identity_document"]},
        {"id": "premises", "name": "Premises verification", "documents": ["lease_or_ownership"]},
        {"id": "business", "name": "Business structure", "documents": ["business_registration"]},
        {"id": "food", "name": "Food-business licensing/registration", **_jk("https://www.fssai.gov.in/business/licensing", "FSSAI — Business Licensing", "Food business operators must be licensed/registered under the FSS Act framework.", ["food_business_details"])},
        {"id": "fire", "name": "Fire-safety requirements", **_jk("https://singlewindow.jk.gov.in/assets/services/procedurechecklist/12/procedurechecklist_file_0721931001649670909.pdf", "J&K Fire & Emergency Services — Provisional NOC checklist", "The J&K checklist identifies site plan, building/floor plan and fire-safety information as required inputs for the cited service.", ["site_plan", "building_plan", "floor_plan", "fire_safety_details"])},
        {"id": "municipal", "name": "Municipal/commercial-establishment requirements", **_jk("https://jansugam.jk.gov.in/getServiceDesc.html?serviceId=16810006", "J&K Municipal Corporation — commercial-establishment NOC service", "The cited service lists premises, identity, building/parking/site information and related NOCs among its inputs depending on applicability.", ["identity_document", "legal_occupancy", "site_plan", "parking_plan", "premises_photo"])},
        {"id": "shops_establishment", "name": "Shops & Establishments registration", **_jk("https://singlewindow.jk.gov.in/assets/services/sop_file/8/sop_file_0304369001648350632.pdf", "J&K Labour & Employment — Shops & Establishments registration", "The J&K SOP lists rent deed/affidavit, employer photograph, identity proof and premises photograph as mandatory inputs for the cited registration service.", ["rent_deed_or_affidavit", "employer_photo", "identity_document", "premises_photo"])},
        {"id": "tax", "name": "Tax registration requirements", "documents": ["tax_details"]},
    ]


def restaurant_tasks() -> List[TaskDefinition]:
    return [
        TaskDefinition("identity_check", "Verify applicant identity", "Identity", "IdentityWorker"),
        TaskDefinition("document_intake", "Extract and validate submitted documents", "Aether", "DocumentWorker"),
        TaskDefinition("premises_check", "Verify premises record and ownership/lease", "Revenue", "RevenueWorker", ["document_intake"]),
        TaskDefinition("business_check", "Validate business structure", "Business Registry", "BusinessWorker", ["document_intake"]),
        TaskDefinition("zoning_check", "Check permitted commercial use", "Municipal", "MunicipalWorker", ["premises_check"]),
        TaskDefinition("tax_check", "Check applicable tax registration", "Tax", "TaxWorker", ["identity_check", "business_check"]),
        TaskDefinition("food_application", "Prepare and submit food-business case", "Food Safety", "FoodWorker", ["document_intake", "business_check"]),
        TaskDefinition("fire_application", "Prepare fire-safety case", "Fire", "FireWorker", ["document_intake", "premises_check"]),
        TaskDefinition("municipal_application", "Prepare municipal/trade case", "Municipal", "MunicipalWorker", ["zoning_check", "tax_check"]),
        TaskDefinition("food_review", "Process food-business response", "Food Safety", "FoodWorker", ["food_application"]),
        TaskDefinition("fire_review", "Process fire response", "Fire", "FireWorker", ["fire_application"]),
        TaskDefinition("municipal_review", "Process municipal response", "Municipal", "MunicipalWorker", ["municipal_application"]),
        TaskDefinition("cross_record_reconciliation", "Reconcile cross-department results", "Aether", "ReconciliationWorker", ["food_review", "fire_review", "municipal_review"]),
        TaskDefinition("inspection", "Physical inspection if legally required", "Authorised Authority", "InspectionCoordinator", ["cross_record_reconciliation"], physical_action=True),
        TaskDefinition("decision_package", "Prepare evidence-backed decision package", "Aether", "DecisionWorker", ["cross_record_reconciliation", "inspection"]),
        TaskDefinition("final_approval", "Statutory final approval/signature", "Authorised Officer", "HumanAuthorityWorker", ["decision_package"], authority_required=True),
        TaskDefinition("record_update", "Update official records after decision", "Aether", "OutcomeWorker", ["final_approval"]),
        TaskDefinition("certificate", "Generate final output/evidence package", "Aether", "OutcomeWorker", ["record_update"]),
    ]


def property_loan_requirements() -> List[Dict]:
    return [{"id": "identity", "name": "Borrower identity", "documents": ["identity_document"]}, {"id": "property", "name": "Property documents", "documents": ["sale_deed", "property_record"]}, {"id": "loan", "name": "Loan case", "documents": ["loan_application"]}]


def property_loan_tasks() -> List[TaskDefinition]:
    return [TaskDefinition("document_intake", "Extract and validate loan/property documents", "Aether", "DocumentWorker"), TaskDefinition("identity_check", "Verify borrower identity", "Identity", "IdentityWorker"), TaskDefinition("land_record", "Retrieve land/property record", "Revenue", "RevenueWorker", ["document_intake"]), TaskDefinition("registration_record", "Retrieve registration record", "Registration", "RegistrationWorker", ["document_intake"]), TaskDefinition("court_search", "Search court/litigation record", "Courts", "CourtWorker", ["document_intake"]), TaskDefinition("tax_dues", "Check property tax/dues", "Tax", "TaxWorker", ["land_record"]), TaskDefinition("encumbrance", "Check encumbrance/security interests", "Registration", "RegistrationWorker", ["registration_record"]), TaskDefinition("document_consistency", "Compare submitted documents", "Aether", "DocumentWorker", ["document_intake", "land_record", "registration_record"]), TaskDefinition("risk_reconciliation", "Reconcile all evidence and identify conflicts", "Aether", "ReconciliationWorker", ["identity_check", "court_search", "tax_dues", "encumbrance", "document_consistency"]), TaskDefinition("legal_review", "Review material exceptions", "Bank Legal", "ExceptionWorker", ["risk_reconciliation"]), TaskDefinition("evidence_package", "Prepare lender evidence package", "Aether", "DecisionWorker", ["risk_reconciliation", "legal_review"]), TaskDefinition("bank_decision", "Return case to lender decision system", "Bank", "OutcomeWorker", ["evidence_package"])]


def commercial_project_tasks() -> List[TaskDefinition]:
    return [TaskDefinition("document_intake", "Extract project and land documents", "Aether", "DocumentWorker"), TaskDefinition("land_title", "Verify land/title", "Revenue", "RevenueWorker", ["document_intake"]), TaskDefinition("court_search", "Search litigation", "Courts", "CourtWorker", ["document_intake"]), TaskDefinition("tax_dues", "Check land/property dues", "Tax", "TaxWorker", ["land_title"]), TaskDefinition("zoning", "Check zoning/land use", "Municipal", "MunicipalWorker", ["land_title"]), TaskDefinition("building", "Prepare building-permission case", "Municipal", "MunicipalWorker", ["zoning"]), TaskDefinition("fire", "Prepare fire-safety case", "Fire", "FireWorker", ["building"]), TaskDefinition("environment", "Prepare environmental case", "Environment", "EnvironmentWorker", ["document_intake"]), TaskDefinition("rera", "Prepare project registration case", "RERA", "RERAWorker", ["land_title", "document_intake"]), TaskDefinition("utility", "Prepare utility requirements", "Utilities", "UtilityWorker", ["building"]), TaskDefinition("reconciliation", "Reconcile cross-department results", "Aether", "ReconciliationWorker", ["court_search", "tax_dues", "fire", "environment", "rera", "utility"]), TaskDefinition("decision_package", "Prepare authority package", "Aether", "DecisionWorker", ["reconciliation"]), TaskDefinition("final_approval", "Statutory decision", "Authorised Officer", "HumanAuthorityWorker", ["decision_package"], authority_required=True), TaskDefinition("outcome", "Complete post-decision records and outputs", "Aether", "OutcomeWorker", ["final_approval"])]


TEMPLATES = {"restaurant": (restaurant_requirements, restaurant_tasks), "property_loan": (property_loan_requirements, property_loan_tasks), "commercial_project": (lambda: [], commercial_project_tasks)}


def infer_template(objective: str, customer_type: str) -> str:
    text = f"{objective} {customer_type}".lower()
    if any(x in text for x in ["restaurant", "cafe", "food business"]): return "restaurant"
    if any(x in text for x in ["loan", "lender", "mortgage", "bank"]): return "property_loan"
    if any(x in text for x in ["project", "factory", "build", "developer"]): return "commercial_project"
    return "commercial_project"
