from __future__ import annotations

from typing import Dict, List

from .domain import TaskDefinition
from .service_registry import ServiceDefinition


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
        {"id": "food", "name": "Food-business licensing/registration", **_jk(
            "https://www.fssai.gov.in/business/licensing",
            "FSSAI — Business Licensing",
            "Food business operators must be licensed/registered under the FSS Act framework.",
            ["food_business_details"],
        )},
        {"id": "fire", "name": "Fire-safety requirements", **_jk(
            "https://singlewindow.jk.gov.in/assets/services/procedurechecklist/12/procedurechecklist_file_0721931001649670909.pdf",
            "J&K Fire & Emergency Services — Provisional NOC checklist",
            "The cited checklist identifies site plan, building/floor plan and fire-safety information as required inputs for the cited service.",
            ["site_plan", "building_plan", "floor_plan", "fire_safety_details"],
        )},
        {"id": "municipal", "name": "Municipal/commercial-establishment requirements", **_jk(
            "https://jansugam.jk.gov.in/getServiceDesc.html?serviceId=16810006",
            "J&K Municipal Corporation — commercial-establishment NOC service",
            "The cited service lists premises, identity, building/parking/site information and related NOCs among its inputs depending on applicability.",
            ["identity_document", "legal_occupancy", "site_plan", "parking_plan", "premises_photo"],
        )},
        {"id": "shops_establishment", "name": "Shops & Establishments registration", **_jk(
            "https://singlewindow.jk.gov.in/assets/services/sop_file/8/sop_file_0304369001648350632.pdf",
            "J&K Labour & Employment — Shops & Establishments registration",
            "The cited SOP lists rent deed/affidavit, employer photograph, identity proof and premises photograph as mandatory inputs for the cited registration service.",
            ["rent_deed_or_affidavit", "employer_photo", "identity_document", "premises_photo"],
        )},
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
    return [
        {"id": "identity", "name": "Borrower identity", "documents": ["identity_document"]},
        {"id": "property", "name": "Property documents", "documents": ["sale_deed", "property_record"]},
        {"id": "loan", "name": "Loan case", "documents": ["loan_application"]},
    ]


def property_loan_tasks() -> List[TaskDefinition]:
    return [
        TaskDefinition("document_intake", "Extract and validate loan/property documents", "Aether", "DocumentWorker"),
        TaskDefinition("identity_check", "Verify borrower identity", "Identity", "IdentityWorker"),
        TaskDefinition("land_record", "Retrieve land/property record", "Revenue", "RevenueWorker", ["document_intake"]),
        TaskDefinition("registration_record", "Retrieve registration record", "Registration", "RegistrationWorker", ["document_intake"]),
        TaskDefinition("court_search", "Search court/litigation record", "Courts", "CourtWorker", ["document_intake"]),
        TaskDefinition("tax_dues", "Check property tax/dues", "Tax", "TaxWorker", ["land_record"]),
        TaskDefinition("encumbrance", "Check encumbrance/security interests", "Registration", "RegistrationWorker", ["registration_record"]),
        TaskDefinition("document_consistency", "Compare submitted documents", "Aether", "DocumentWorker", ["document_intake", "land_record", "registration_record"]),
        TaskDefinition("risk_reconciliation", "Reconcile all evidence and identify conflicts", "Aether", "ReconciliationWorker", ["identity_check", "court_search", "tax_dues", "encumbrance", "document_consistency"]),
        TaskDefinition("legal_review", "Review material exceptions", "Bank Legal", "ExceptionWorker", ["risk_reconciliation"]),
        TaskDefinition("evidence_package", "Prepare lender evidence package", "Aether", "DecisionWorker", ["risk_reconciliation", "legal_review"]),
        TaskDefinition("bank_decision", "Return case to lender decision system", "Bank", "OutcomeWorker", ["evidence_package"]),
    ]


def commercial_project_tasks() -> List[TaskDefinition]:
    return [
        TaskDefinition("document_intake", "Extract project and land documents", "Aether", "DocumentWorker"),
        TaskDefinition("land_title", "Verify land/title", "Revenue", "RevenueWorker", ["document_intake"]),
        TaskDefinition("court_search", "Search litigation", "Courts", "CourtWorker", ["document_intake"]),
        TaskDefinition("tax_dues", "Check land/property dues", "Tax", "TaxWorker", ["land_title"]),
        TaskDefinition("zoning", "Check zoning/land use", "Municipal", "MunicipalWorker", ["land_title"]),
        TaskDefinition("building", "Prepare building-permission case", "Municipal", "MunicipalWorker", ["zoning"]),
        TaskDefinition("fire", "Prepare fire-safety case", "Fire", "FireWorker", ["building"]),
        TaskDefinition(
            "site_inspection",
            "Physical project/site inspection by authorised authority",
            "Authorised Authority",
            "InspectionCoordinator",
            ["building", "fire"],
            physical_action=True,
            operation="inspection",
            description="Aether prepares the inspection packet; only an authorised inspector records findings.",
        ),
        TaskDefinition("environment", "Prepare environmental case", "Environment", "EnvironmentWorker", ["document_intake"]),
        TaskDefinition("rera", "Prepare project registration case", "RERA", "RERAWorker", ["land_title", "document_intake"]),
        TaskDefinition("utility", "Prepare utility requirements", "Utilities", "UtilityWorker", ["building"]),
        TaskDefinition("reconciliation", "Reconcile cross-department results", "Aether", "ReconciliationWorker", ["court_search", "tax_dues", "fire", "environment", "rera", "utility", "site_inspection"]),
        TaskDefinition("decision_package", "Prepare authority package", "Aether", "DecisionWorker", ["reconciliation"]),
        TaskDefinition("final_approval", "Statutory decision", "Authorised Officer", "HumanAuthorityWorker", ["decision_package"], authority_required=True),
        TaskDefinition("outcome", "Complete post-decision records and outputs", "Aether", "OutcomeWorker", ["final_approval"]),
    ]


def _service_worker(service: ServiceDefinition) -> str:
    return {
        "Revenue": "RevenueWorker",
        "Registration": "RegistrationWorker",
        "Municipal": "MunicipalWorker",
        "Health": "HealthWorker",
        "Education": "EducationWorker",
        "Transport": "TransportWorker",
        "Labour": "LabourWorker",
        "Tax": "TaxWorker",
        "Corporate Registry": "CorporateRegistryWorker",
        "Food & Civil Supplies": "CivilSuppliesWorker",
        "Police": "PoliceWorker",
        "Agriculture": "AgricultureWorker",
        "Housing": "HousingWorker",
        "RERA": "RERAWorker",
        "Courts": "CourtWorker",
        "Passport": "PassportWorker",
        "Food Safety": "FoodWorker",
    }.get(service.department, "DigitalWorker")


def _finish_service_tasks(service: ServiceDefinition, tasks: List[TaskDefinition], parent: str) -> List[TaskDefinition]:
    tasks.append(TaskDefinition(
        "decision_package",
        "Prepare evidence-backed outcome package",
        "Aether",
        "DecisionWorker",
        [parent],
        description="Assemble verified evidence for the statutory or operational outcome.",
        operation="decision_package",
    ))
    if service.human_authority_required:
        tasks.append(TaskDefinition(
            "final_approval",
            "Authorised human decision",
            "Authorised Authority",
            "HumanAuthorityWorker",
            ["decision_package"],
            authority_required=True,
            description="Aether stops here when law requires an authorised human decision.",
            operation="final_approval",
        ))
        parent = "final_approval"
    tasks.append(TaskDefinition(
        "outcome",
        f"Complete {service.outcome}",
        "Aether",
        "OutcomeWorker",
        [parent],
        operation="outcome",
    ))
    return tasks


def generic_tasks(service: ServiceDefinition) -> List[TaskDefinition]:
    """Build a reusable, auditable process graph for catalog services.

    The graph is deliberately broader than a single department form:
    identity/document work runs first, applicable government records are checked
    in parallel where possible, results are reconciled, and only then does the
    case cross the human-authority boundary. Service-specific legal graphs can
    replace this safe baseline as authoritative rules and connectors are added.
    """
    worker = _service_worker(service)
    sid = service.id

    # Property and land workflows need independent evidence checks before a
    # statutory outcome. These tasks share the same backbone used by bank and
    # developer cases without pretending every service has the same legal rule.
    property_services = {
        "property_registration",
        "mutation",
        "encumbrance_certificate",
        "land_conversion",
        "title_verification",
    }
    if sid in property_services:
        tasks = [
            TaskDefinition("document_intake", f"Extract and validate {service.name} inputs", "Aether", "DocumentWorker", operation="document"),
            TaskDefinition("identity_check", "Verify applicant/subject identity", "Identity", "IdentityWorker", operation="identity"),
            TaskDefinition("land_record", "Retrieve land/property record", "Revenue", "RevenueWorker", ["document_intake"], operation="land_record"),
            TaskDefinition("registration_record", "Retrieve registration record", "Registration", "RegistrationWorker", ["document_intake"], operation="registration_record"),
            TaskDefinition("court_search", "Search litigation record", "Courts", "CourtWorker", ["document_intake"], operation="court_search"),
            TaskDefinition("tax_dues", "Check property/land dues", "Tax", "TaxWorker", ["land_record"], operation="tax_dues"),
            TaskDefinition("cross_record_reconciliation", "Reconcile material government records", "Aether", "ReconciliationWorker", ["identity_check", "court_search", "tax_dues", "registration_record"], operation="reconciliation"),
        ]
        return _finish_service_tasks(service, tasks, "cross_record_reconciliation")

    # Identity/document-heavy certificates and reports.
    if sid in {"birth_certificate", "death_certificate"}:
        record_operation = "birth_record" if sid == "birth_certificate" else "death_record"
        tasks = [
            TaskDefinition("document_intake", f"Validate {service.name} evidence", "Aether", "DocumentWorker", operation="document"),
            TaskDefinition("identity_check", "Verify applicant identity", "Identity", "IdentityWorker", operation="identity"),
            TaskDefinition("record_lookup", f"Retrieve {service.name.lower()} record", "Health", "HealthWorker", ["document_intake", "identity_check"], operation=record_operation),
            TaskDefinition("verification", "Verify source record and submitted evidence", "Aether", "ReconciliationWorker", ["record_lookup"], operation="reconciliation"),
        ]
        return _finish_service_tasks(service, tasks, "verification")

    if sid in {"police_clearance", "fir_report"}:
        tasks = [
            TaskDefinition("document_intake", f"Validate {service.name} request", "Aether", "DocumentWorker", operation="document"),
            TaskDefinition("identity_check", "Verify applicant identity", "Identity", "IdentityWorker", operation="identity"),
            TaskDefinition("police_search", "Search police records", "Police", "PoliceWorker", ["document_intake", "identity_check"], operation="police_search"),
            TaskDefinition("verification", "Verify police source response", "Aether", "ReconciliationWorker", ["police_search"], operation="reconciliation"),
        ]
        return _finish_service_tasks(service, tasks, "verification")

    # Passport/visa processes can require external verification before an
    # authorised issuance decision.
    if sid in {"passport", "visa"}:
        tasks = [
            TaskDefinition("document_intake", f"Validate {service.name} evidence", "Aether", "DocumentWorker", operation="document"),
            TaskDefinition("identity_check", "Verify identity", "Identity", "IdentityWorker", operation="identity"),
            TaskDefinition("address_check", "Verify address/residency evidence", "Identity", "IdentityWorker", ["document_intake"], operation="address"),
            TaskDefinition("police_verification", "Request police verification when applicable", "Police", "PoliceWorker", ["identity_check", "address_check"], operation="police_verification"),
            TaskDefinition("department_processing", f"Process {service.name} case", "Passport", "PassportWorker", ["document_intake", "identity_check", "police_verification"], operation="service_processing"),
            TaskDefinition("verification", "Reconcile passport/visa evidence", "Aether", "ReconciliationWorker", ["department_processing"], operation="reconciliation"),
        ]
        return _finish_service_tasks(service, tasks, "verification")

    # Transport services may cross a physical-action boundary such as a test or
    # inspection. That boundary is explicit rather than hidden in automation.
    if sid in {"driving_license", "vehicle_registration"}:
        physical_name = "driving_test" if sid == "driving_license" else "vehicle_inspection"
        physical_desc = "Physical driving test by authorised authority" if sid == "driving_license" else "Physical vehicle inspection by authorised authority"
        tasks = [
            TaskDefinition("document_intake", f"Validate {service.name} documents", "Aether", "DocumentWorker", operation="document"),
            TaskDefinition("identity_check", "Verify identity", "Identity", "IdentityWorker", operation="identity"),
            TaskDefinition("department_processing", f"Process {service.name} digital checks", service.department, worker, ["document_intake", "identity_check"], operation="service_processing"),
            TaskDefinition(physical_name, physical_desc, "Authorised Authority", "InspectionCoordinator", ["department_processing"], physical_action=True, operation="inspection"),
            TaskDefinition("verification", "Verify transport evidence and inspection result", "Aether", "ReconciliationWorker", [physical_name], operation="reconciliation"),
        ]
        return _finish_service_tasks(service, tasks, "verification")

    if sid in {"company_registration", "gst_registration"}:
        if sid == "company_registration":
            department_task = TaskDefinition(
                "corporate_registry",
                "Process company incorporation record",
                "Corporate Registry",
                "CorporateRegistryWorker",
                ["document_intake", "identity_check"],
                operation="service_processing",
            )
            tax_dependency = "corporate_registry"
        else:
            department_task = TaskDefinition(
                "tax_registration",
                "Process GST registration",
                "Tax",
                "TaxWorker",
                ["document_intake", "identity_check"],
                operation="service_processing",
            )
            tax_dependency = "tax_registration"
        tasks = [
            TaskDefinition("document_intake", f"Validate {service.name} inputs", "Aether", "DocumentWorker", operation="document"),
            TaskDefinition("identity_check", "Verify applicant identity", "Identity", "IdentityWorker", operation="identity"),
            department_task,
            TaskDefinition(
                "tax_record",
                "Cross-check tax identity and registration status",
                "Tax",
                "TaxWorker",
                ["identity_check", tax_dependency],
                operation="tax_verification",
            ),
            TaskDefinition(
                "cross_record_reconciliation",
                "Reconcile incorporation/tax records",
                "Aether",
                "ReconciliationWorker",
                ["corporate_registry" if sid == "company_registration" else "tax_registration", "tax_record"],
                operation="reconciliation",
            ),
        ]
        return _finish_service_tasks(service, tasks, "cross_record_reconciliation")

    if sid in {"trade_license", "building_permit"}:
        tasks = [
            TaskDefinition("document_intake", f"Validate {service.name} documents", "Aether", "DocumentWorker", operation="document"),
            TaskDefinition("identity_check", "Verify applicant identity", "Identity", "IdentityWorker", operation="identity"),
            TaskDefinition("land_record", "Retrieve property/land record", "Revenue", "RevenueWorker", ["document_intake"], operation="land_record"),
            TaskDefinition("zoning_check", "Verify zoning and permitted use", "Municipal", "MunicipalWorker", ["land_record"], operation="zoning"),
            TaskDefinition("tax_dues", "Check municipal/property dues", "Tax", "TaxWorker", ["land_record"], operation="tax_dues"),
            TaskDefinition(
                "fire_check",
                "Check fire-safety requirements",
                "Fire",
                "FireWorker",
                ["document_intake"],
                operation="fire",
            ),
            TaskDefinition(
                "premises_inspection",
                "Physical premises/site inspection by authorised authority",
                "Authorised Authority",
                "InspectionCoordinator",
                ["zoning_check", "fire_check"],
                physical_action=True,
                operation="inspection",
                description="Aether prepares and schedules the inspection; only the authorised inspector can record the finding.",
            ),
            TaskDefinition(
                "municipal_processing",
                f"Process {service.name} departmental review",
                "Municipal",
                "MunicipalWorker",
                ["identity_check", "zoning_check", "tax_dues", "fire_check", "premises_inspection"],
                operation="service_processing",
            ),
            TaskDefinition(
                "cross_record_reconciliation",
                "Reconcile property, zoning, tax, safety and inspection evidence",
                "Aether",
                "ReconciliationWorker",
                ["municipal_processing", "land_record", "zoning_check", "tax_dues", "fire_check", "premises_inspection"],
                operation="reconciliation",
            ),
        ]
        return _finish_service_tasks(service, tasks, "cross_record_reconciliation")

    if sid == "factory_license":
        tasks = [
            TaskDefinition("document_intake", "Validate factory licence evidence", "Aether", "DocumentWorker", operation="document"),
            TaskDefinition("identity_check", "Verify applicant/company identity", "Identity", "IdentityWorker", operation="identity"),
            TaskDefinition("land_record", "Verify factory premises record", "Revenue", "RevenueWorker", ["document_intake"], operation="land_record"),
            TaskDefinition("labour_compliance", "Check labour registration/compliance", "Labour", "LabourWorker", ["identity_check"], operation="labour_compliance"),
            TaskDefinition("fire_check", "Check fire-safety compliance", "Fire", "FireWorker", ["document_intake"], operation="fire"),
            TaskDefinition("environment_check", "Check environmental consent status", "Environment", "EnvironmentWorker", ["document_intake"], operation="environment"),
            TaskDefinition(
                "factory_processing",
                "Process factory licence application",
                "Labour",
                "LabourWorker",
                ["land_record", "labour_compliance", "fire_check", "environment_check"],
                operation="service_processing",
            ),
            TaskDefinition(
                "cross_record_reconciliation",
                "Reconcile labour, premises, fire and environment evidence",
                "Aether",
                "ReconciliationWorker",
                ["factory_processing", "land_record", "labour_compliance", "fire_check", "environment_check"],
                operation="reconciliation",
            ),
        ]
        return _finish_service_tasks(service, tasks, "cross_record_reconciliation")

    if sid == "rera_registration":
        tasks = [
            TaskDefinition("document_intake", "Validate RERA project evidence", "Aether", "DocumentWorker", operation="document"),
            TaskDefinition("identity_check", "Verify promoter identity/company", "Identity", "IdentityWorker", operation="identity"),
            TaskDefinition("land_record", "Verify project land record", "Revenue", "RevenueWorker", ["document_intake"], operation="land_record"),
            TaskDefinition("title_check", "Verify project title evidence", "Revenue", "RevenueWorker", ["land_record"], operation="title_check"),
            TaskDefinition("court_search", "Search project litigation records", "Courts", "CourtWorker", ["land_record"], operation="court_search"),
            TaskDefinition("tax_dues", "Check project/property dues", "Tax", "TaxWorker", ["land_record"], operation="tax_dues"),
            TaskDefinition("building_check", "Review building/project planning evidence", "Municipal", "MunicipalWorker", ["document_intake"], operation="building"),
            TaskDefinition("fire_check", "Check project fire-safety evidence", "Fire", "FireWorker", ["document_intake"], operation="fire"),
            TaskDefinition(
                "rera_processing",
                "Process RERA registration",
                "RERA",
                "RERAWorker",
                ["identity_check", "title_check", "court_search", "tax_dues", "building_check", "fire_check"],
                operation="service_processing",
            ),
            TaskDefinition(
                "cross_record_reconciliation",
                "Reconcile land, court, tax, planning and safety evidence",
                "Aether",
                "ReconciliationWorker",
                ["rera_processing", "title_check", "court_search", "tax_dues", "building_check", "fire_check"],
                operation="reconciliation",
            ),
        ]
        return _finish_service_tasks(service, tasks, "cross_record_reconciliation")

    if sid in {"farmer_id", "crop_insurance"}:
        record_task = "farmer_record" if sid == "farmer_id" else "crop_record"
        record_operation = "farmer_record" if sid == "farmer_id" else "crop_record"
        tasks = [
            TaskDefinition("document_intake", f"Validate {service.name} evidence", "Aether", "DocumentWorker", operation="document"),
            TaskDefinition("identity_check", "Verify farmer identity", "Identity", "IdentityWorker", operation="identity"),
            TaskDefinition("land_record", "Verify agricultural land record", "Revenue", "RevenueWorker", ["document_intake"], operation="land_record"),
            TaskDefinition(record_task, f"Retrieve {service.name.lower()} record", "Agriculture", "AgricultureWorker", ["identity_check"], operation=record_operation),
            TaskDefinition("eligibility", "Check benefit/insurance eligibility", "Agriculture", "AgricultureWorker", ["land_record", record_task], operation="eligibility"),
            TaskDefinition(
                "cross_record_reconciliation",
                "Reconcile identity, land and agriculture evidence",
                "Aether",
                "ReconciliationWorker",
                ["identity_check", "land_record", record_task, "eligibility"],
                operation="reconciliation",
            ),
        ]
        return _finish_service_tasks(service, tasks, "cross_record_reconciliation")

    if sid in {"medical_license", "ration_card", "scholarship"}:
        if sid == "medical_license":
            tasks = [
                TaskDefinition("document_intake", "Validate medical licence evidence", "Aether", "DocumentWorker", operation="document"),
                TaskDefinition("identity_check", "Verify applicant/professional identity", "Identity", "IdentityWorker", operation="identity"),
                TaskDefinition("professional_registry", "Verify professional registration", "Health", "HealthWorker", ["identity_check"], operation="professional_registry"),
                TaskDefinition("premises_check", "Check health premises evidence", "Health", "HealthWorker", ["document_intake"], operation="premises"),
                TaskDefinition("inspection", "Physical premises inspection where legally required", "Authorised Authority", "InspectionCoordinator", ["premises_check"], physical_action=True, operation="inspection"),
                TaskDefinition("health_processing", "Process medical licence case", "Health", "HealthWorker", ["professional_registry", "inspection"], operation="service_processing"),
                TaskDefinition("cross_record_reconciliation", "Reconcile professional, premises and inspection evidence", "Aether", "ReconciliationWorker", ["health_processing"], operation="reconciliation"),
            ]
        elif sid == "ration_card":
            tasks = [
                TaskDefinition("document_intake", "Validate household eligibility evidence", "Aether", "DocumentWorker", operation="document"),
                TaskDefinition("identity_check", "Verify household applicant identity", "Identity", "IdentityWorker", operation="identity"),
                TaskDefinition("household_record", "Check household/beneficiary record", "Food & Civil Supplies", "CivilSuppliesWorker", ["identity_check"], operation="household_record"),
                TaskDefinition("duplicate_check", "Check for duplicate ration benefits", "Food & Civil Supplies", "CivilSuppliesWorker", ["identity_check"], operation="duplicate_check"),
                TaskDefinition("eligibility", "Check scheme eligibility", "Food & Civil Supplies", "CivilSuppliesWorker", ["household_record", "duplicate_check"], operation="eligibility"),
                TaskDefinition("cross_record_reconciliation", "Reconcile identity, household and eligibility evidence", "Aether", "ReconciliationWorker", ["eligibility"], operation="reconciliation"),
            ]
        else:
            tasks = [
                TaskDefinition("document_intake", "Validate scholarship evidence", "Aether", "DocumentWorker", operation="document"),
                TaskDefinition("identity_check", "Verify student identity", "Identity", "IdentityWorker", operation="identity"),
                TaskDefinition("education_record", "Verify education/enrolment record", "Education", "EducationWorker", ["identity_check"], operation="education_record"),
                TaskDefinition("eligibility", "Check scholarship eligibility", "Education", "EducationWorker", ["education_record", "document_intake"], operation="eligibility"),
                TaskDefinition("bank_check", "Verify beneficiary payment details", "Finance", "FinanceWorker", ["identity_check"], operation="beneficiary_check"),
                TaskDefinition("cross_record_reconciliation", "Reconcile student, eligibility and payment evidence", "Aether", "ReconciliationWorker", ["eligibility", "bank_check"], operation="reconciliation"),
            ]
        return _finish_service_tasks(service, tasks, "cross_record_reconciliation")

    # All other services receive the same safe end-to-end baseline. This is
    # intentionally not described as the service's authoritative legal process.
    tasks = [
        TaskDefinition("document_intake", f"Validate {service.name} inputs", "Aether", "DocumentWorker", operation="document"),
        TaskDefinition("identity_check", "Verify subject identity", "Identity", "IdentityWorker", operation="identity"),
        TaskDefinition(
            "department_processing",
            f"Execute {service.name} departmental work",
            service.department,
            worker,
            ["document_intake", "identity_check"],
            operation="service_processing",
            description="Execute the authorized digital work available through the department connector.",
        ),
        TaskDefinition(
            "verification",
            "Verify and reconcile service result",
            "Aether",
            "ReconciliationWorker",
            ["department_processing"],
            operation="reconciliation",
        ),
    ]
    return _finish_service_tasks(service, tasks, "verification")


def generic_requirements(service: ServiceDefinition) -> List[Dict]:
    return [{
        "id": "service_intake",
        "name": f"Inputs for {service.name}",
        "documents": service.documents(),
        "confidence": "service-registry-mvp",
        "reason": "Baseline input set from Aether's service metadata; legal requirements must be verified before production automation.",
    }]


TEMPLATES = {
    "restaurant": (restaurant_requirements, restaurant_tasks),
    "property_loan": (property_loan_requirements, property_loan_tasks),
    "commercial_project": (lambda: [], commercial_project_tasks),
}


def infer_template(objective: str, customer_type: str, service: ServiceDefinition | None = None) -> str:
    text = f"{objective} {customer_type}".lower()
    # Templates are only selected when the objective actually supports the
    # specialized workflow. A service being related to a domain is not enough;
    # this prevents a simple trade licence or property registration request
    # from silently becoming a restaurant/project workflow.
    if service and service.template == "restaurant":
        return "restaurant" if any(x in text for x in ["restaurant", "cafe", "food business", "food license", "fssai"]) else "generic"
    if service and service.template == "property_loan":
        return "property_loan" if any(x in text for x in ["loan", "lender", "mortgage", "bank"]) else "generic"
    if service and service.template == "commercial_project":
        return "commercial_project" if any(x in text for x in ["project", "factory", "construction", "developer"]) else "generic"
    if any(x in text for x in ["restaurant", "cafe", "food business"]):
        return "restaurant"
    if any(x in text for x in ["loan", "lender", "mortgage", "bank"]):
        return "property_loan"
    if any(x in text for x in ["project", "factory", "build", "developer"]):
        return "commercial_project"
    return "generic"
