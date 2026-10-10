from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .domain import TaskDefinition
from .service_registry import ServiceDefinition
from .process_work_recipes import work_recipe, atom_task_mapping, work_atom_metadata


@dataclass(frozen=True)
class GovernmentProcessProfile:
    key: str
    label: str
    payment_sensitive: bool = False
    committee_review: bool = False
    interdepartmental: bool = False
    post_decision_followup: bool = True


SERVICE_PROCESS_PROFILES = {
    "property_registration": GovernmentProcessProfile("property_registration", "Property registration"),
    "mutation": GovernmentProcessProfile("land_mutation", "Land-record mutation"),
    "encumbrance_certificate": GovernmentProcessProfile("property_record", "Property record/certificate"),
    "title_verification": GovernmentProcessProfile("property_record", "Property title verification"),
    "land_conversion": GovernmentProcessProfile("land_conversion", "Land-use conversion", payment_sensitive=True),
    "trade_license": GovernmentProcessProfile("municipal_license", "Municipal licence", payment_sensitive=True),
    "building_permit": GovernmentProcessProfile(
        "building_permit",
        "Building/development permission",
        payment_sensitive=True,
        committee_review=True,
        interdepartmental=True,
    ),
    "water_connection": GovernmentProcessProfile("utility_connection", "Utility connection", payment_sensitive=True),
    "birth_certificate": GovernmentProcessProfile("certificate", "Certificate/record issuance"),
    "death_certificate": GovernmentProcessProfile("certificate", "Certificate/record issuance"),
    "medical_license": GovernmentProcessProfile(
        "regulated_professional_license",
        "Regulated professional licence",
        committee_review=False,
        interdepartmental=True,
    ),
    "scholarship": GovernmentProcessProfile("benefit", "Scholarship/benefit", payment_sensitive=True),
    "admission": GovernmentProcessProfile("education", "Education admission"),
    "transfer_certificate": GovernmentProcessProfile("certificate", "Certificate/record issuance"),
    "driving_license": GovernmentProcessProfile("transport_license", "Driving licence"),
    "vehicle_registration": GovernmentProcessProfile("vehicle_registration", "Vehicle registration", payment_sensitive=True),
    "factory_license": GovernmentProcessProfile(
        "factory_license",
        "Factory/labour licence",
        payment_sensitive=True,
        committee_review=True,
        interdepartmental=True,
    ),
    "pf_esi_registration": GovernmentProcessProfile("labour_registration", "Labour/social-security registration"),
    "gst_registration": GovernmentProcessProfile("tax_registration", "Tax registration"),
    "company_registration": GovernmentProcessProfile("corporate_incorporation", "Corporate incorporation"),
    "ration_card": GovernmentProcessProfile("benefit", "Entitlement/benefit"),
    "pds_subsidy": GovernmentProcessProfile("benefit", "Entitlement/benefit", payment_sensitive=True),
    "police_clearance": GovernmentProcessProfile("certificate", "Police certificate"),
    "fir_report": GovernmentProcessProfile("police_record", "Police record/service"),
    "farmer_id": GovernmentProcessProfile("benefit", "Farmer registration"),
    "crop_insurance": GovernmentProcessProfile("benefit", "Farmer benefit/insurance", payment_sensitive=True),
    "pmay": GovernmentProcessProfile("benefit", "Housing benefit", payment_sensitive=True),
    "affordable_housing": GovernmentProcessProfile(
        "project_approval",
        "Housing/project approval",
        payment_sensitive=True,
        interdepartmental=True,
    ),
    "rera_registration": GovernmentProcessProfile(
        "regulated_project",
        "Regulated real-estate project registration",
        payment_sensitive=True,
        committee_review=True,
        interdepartmental=True,
    ),
    "court_case_filing": GovernmentProcessProfile("adjudication", "Judicial/adjudicatory filing"),
    "e_court": GovernmentProcessProfile("adjudication", "Judicial/adjudicatory service"),
    "passport": GovernmentProcessProfile("passport", "Passport/consular workflow", interdepartmental=True),
    "visa": GovernmentProcessProfile("passport", "Visa workflow", interdepartmental=True),
    "food_business_license": GovernmentProcessProfile(
        "food_license",
        "Food-business licence/registration",
        payment_sensitive=True,
        interdepartmental=True,
    ),
}


_DEPARTMENT_PROCESS_DEFAULTS = {
    "revenue": GovernmentProcessProfile("record_or_revenue", "Revenue/land record case"),
    "registration": GovernmentProcessProfile("registration", "Registration/record case"),
    "municipal": GovernmentProcessProfile("municipal_license", "Municipal service", payment_sensitive=True),
    "health": GovernmentProcessProfile("health_regulatory", "Health/medical service", interdepartmental=True),
    "education": GovernmentProcessProfile("education", "Education service"),
    "transport": GovernmentProcessProfile("transport", "Transport service", payment_sensitive=True),
    "labour": GovernmentProcessProfile("labour", "Labour/employment service", interdepartmental=True),
    "tax": GovernmentProcessProfile("tax", "Tax service", payment_sensitive=True),
    "corporate registry": GovernmentProcessProfile("corporate", "Corporate registry service"),
    "food & civil supplies": GovernmentProcessProfile("benefit", "Food entitlement/benefit", payment_sensitive=True),
    "police": GovernmentProcessProfile("police", "Police service", interdepartmental=True),
    "agriculture": GovernmentProcessProfile("agriculture", "Agriculture service", interdepartmental=True),
    "housing": GovernmentProcessProfile("housing", "Housing/project service", payment_sensitive=True, interdepartmental=True),
    "rera": GovernmentProcessProfile("regulated_project", "Regulated project service", payment_sensitive=True, interdepartmental=True),
    "courts": GovernmentProcessProfile("adjudication", "Judicial/adjudicatory service"),
    "passport": GovernmentProcessProfile("passport", "Passport service", interdepartmental=True),
    "fire": GovernmentProcessProfile("fire_safety", "Fire-safety service", interdepartmental=True),
    "environment": GovernmentProcessProfile("environment", "Environment/regulatory service", interdepartmental=True),
    "forest": GovernmentProcessProfile("environment", "Forest/environment permission", interdepartmental=True),
    "mines": GovernmentProcessProfile("regulated_resource", "Mining/resource service", payment_sensitive=True, interdepartmental=True),
    "grievance": GovernmentProcessProfile("grievance", "Public grievance"),
    "information commission": GovernmentProcessProfile("information_access", "Information-access service"),
    "procurement": GovernmentProcessProfile("procurement", "Public procurement", payment_sensitive=True, interdepartmental=True),
    "pension": GovernmentProcessProfile("benefit", "Pension service", payment_sensitive=True),
    "social welfare": GovernmentProcessProfile("benefit", "Social welfare service", payment_sensitive=True),
    "electricity": GovernmentProcessProfile("utility_connection", "Electricity utility service", payment_sensitive=True),
    "utilities": GovernmentProcessProfile("utility_connection", "Utility service", payment_sensitive=True),
    "consumer affairs": GovernmentProcessProfile("consumer", "Consumer/regulatory service"),
    "rural development": GovernmentProcessProfile("rural_development", "Rural development service", interdepartmental=True),
    "skill/employment": GovernmentProcessProfile("employment", "Skill/employment service"),
    "employment": GovernmentProcessProfile("employment", "Employment service"),
}


def infer_process_profile(
    service: ServiceDefinition | None,
    task_definitions: Iterable[TaskDefinition] = (),
) -> GovernmentProcessProfile:
    if service and service.id in SERVICE_PROCESS_PROFILES:
        profile = SERVICE_PROCESS_PROFILES[service.id]
    else:
        departments = {
            task.department.strip().lower()
            for task in task_definitions
            if task.department.strip().lower() not in {"aether", "authorised authority", "authorised officer"}
        }
        if len(departments) > 1:
            return GovernmentProcessProfile("multi_department", "Multi-department case", interdepartmental=True)
        if departments:
            department = next(iter(departments))
            return _DEPARTMENT_PROCESS_DEFAULTS.get(
                department,
                GovernmentProcessProfile("generic", "Government service")
            )
        if service:
            return _DEPARTMENT_PROCESS_DEFAULTS.get(
                service.department.strip().lower(),
                GovernmentProcessProfile("generic", "Government service")
            )
        return GovernmentProcessProfile("generic", "Government service")

    if not profile.interdepartmental:
        departments = {
            task.department.strip().lower()
            for task in task_definitions
            if task.department.strip().lower() not in {"aether", "authorised authority", "authorised officer"}
        }
        if len(departments) > 1:
            return GovernmentProcessProfile(
                profile.key,
                profile.label,
                payment_sensitive=profile.payment_sensitive,
                committee_review=profile.committee_review,
                interdepartmental=True,
                post_decision_followup=profile.post_decision_followup,
            )
    return profile


def _task(
    task_id: str,
    name: str,
    operation: str,
    dependencies: List[str] | None = None,
    description: str = "",
) -> TaskDefinition:
    return TaskDefinition(
        id=task_id,
        name=name,
        department="Aether",
        worker="AdministrativeWorker",
        dependencies=list(dependencies or []),
        description=description,
        operation=operation,
    )


def build_administrative_tasks(
    service: ServiceDefinition | None,
    original_tasks: List[TaskDefinition],
) -> List[TaskDefinition]:
    profile = infer_process_profile(service, original_tasks)
    original_ids = [task.id for task in original_tasks]
    document_ids = [task.id for task in original_tasks if task.worker == "DocumentWorker"]
    identity_ids = [task.id for task in original_tasks if task.operation == "identity" or task.id == "identity_check"]
    physical = [task for task in original_tasks if task.physical_action]
    processing = [
        task.id for task in original_tasks
        if task.worker != "Aether"
        and not task.authority_required
        and not task.physical_action
        and task.id not in {"document_intake", "identity_check"}
    ]
    shared = ["internal_case_triage"]
    tasks = [
        _task(
            "internal_case_triage",
            "Automatic case triage and routing",
            "case_triage",
            description="Classify priority, jurisdiction and operating context before staff work begins.",
        ),
        _task(
            "internal_case_file",
            "Automatic case-file assembly",
            "case_file_assembly",
            ["internal_case_triage"],
            "Assemble the working file, document checklist and deficiency baseline.",
        ),
        _task(
            "internal_data_normalization",
            "Automatic data normalization",
            "data_normalization",
            ["internal_case_file"] + document_ids[:1],
            "Normalize identities, identifiers and references for downstream work.",
        ),
        _task(
            "internal_assignment",
            "Automatic section and workload assignment",
            "assignment",
            ["internal_case_triage", "internal_data_normalization"],
            "Recommend the correct section/official using jurisdiction, service, priority and available context.",
        ),
        _task(
            "internal_form_prep",
            "Automatic departmental form preparation",
            "form_prep",
            ["internal_data_normalization"],
            "Map verified facts into a downstream form/register-ready payload with field provenance.",
        ),
        _task(
            "internal_case_notes",
            "Automatic scrutiny and case-note preparation",
            "case_notes",
            ["internal_data_normalization"],
            "Prepare chronology, key facts, open issues and the next official action.",
        ),
        _task(
            "internal_deficiency",
            "Automatic deficiency and clarification preparation",
            "deficiency",
            ["internal_case_file", "internal_data_normalization"],
            "Convert missing or inconsistent evidence into precise applicant-fixable deficiencies.",
        ),
        _task(
            "internal_query_response",
            "Automatic government-query response packet",
            "query_response",
            ["internal_case_notes", "internal_deficiency"],
            "Collect the current evidence relevant to a government query and prepare a response packet for authorised review.",
        ),
        _task(
            "internal_correspondence",
            "Automatic correspondence preparation",
            "correspondence",
            ["internal_deficiency", "internal_case_notes"],
            "Prepare missing-document, query and progress communications for dispatch.",
        ),
        _task(
            "internal_followup_plan",
            "Automatic follow-up planning",
            "followup_plan",
            ["internal_assignment", "internal_deficiency"],
            "Generate next follow-ups for pending, queried and dependency-blocked work.",
        ),
        _task(
            "internal_sla_snapshot",
            "Automatic SLA and pending-risk snapshot",
            "sla_snapshot",
            ["internal_case_triage", "internal_assignment"],
            "Identify ageing work, dependency waits and cases needing escalation.",
        ),
        _task(
            "internal_interim_response",
            "Automatic interim progress / deficiency response",
            "interim_response",
            ["internal_followup_plan", "internal_sla_snapshot"],
            "Explain what is waiting or missing without requiring the applicant to restart the case.",
        ),
        _task(
            "internal_preflight_check",
            "Automatic pre-submission scrutiny",
            "preflight_check",
            ["internal_case_file", "internal_data_normalization", "internal_continuity_review"],
            "Catch missing evidence, conflicting identifiers and known recurring issues before downstream government submission.",
        ),
        _task(
            "internal_recovery_plan",
            "Automatic exception recovery and replan",
            "recovery_plan",
            ["internal_followup_plan", "internal_sla_snapshot"],
            "Preserve case state and verified evidence while identifying retry and affected branches.",
        ),
    ]

    if profile.interdepartmental or len({task.department for task in original_tasks if task.department != "Aether"}) > 1:
        tasks.append(
            _task(
                "internal_interdepartment_handoff",
                "Automatic inter-department handoff packet",
                "interdepartment_handoff",
                ["internal_form_prep", "internal_case_notes"],
                "Prepare structured requests and response packets between departments.",
            )
        )

    if physical:
        physical_ids = [task.id for task in physical]
        prerequisites = sorted({
            dependency
            for task in physical
            for dependency in task.dependencies
            if dependency in original_ids
        })
        deps = ["internal_case_file", "internal_form_prep"]
        deps.extend(prerequisites)
        tasks.append(
            _task(
                "internal_inspection_packet",
                "Automatic inspection / field-verification packet",
                "inspection_packet",
                list(dict.fromkeys(deps)),
                "Prepare the officer visit packet and checklist without fabricating the inspection result.",
            )
        )

    if profile.payment_sensitive:
        payment_deps = ["internal_case_file", "internal_data_normalization"]
        if processing:
            payment_deps.append(processing[-1])
        tasks.append(
            _task(
                "internal_fee_reconciliation",
                "Automatic fee, demand and payment reconciliation",
                "fee_reconciliation",
                list(dict.fromkeys(payment_deps)),
                "Reconcile known demand/payment records and surface any balance or mismatch.",
            )
        )

    # Materialize recipe steps that are not already represented by a service
    # task or one of the deeper administration primitives above. These nodes
    # make employee work explicit and executable through authorised connectors.
    existing_task_ids = {task.id for task in original_tasks} | {task.id for task in tasks}
    recipe = work_recipe(profile.key)
    atom_mapping = atom_task_mapping()
    atom_meta = work_atom_metadata()

    # Materialize mapped high-level atoms with stable internal task IDs.
    # This keeps the graph/API vocabulary deterministic and lets operators
    # trace a conceptual work atom to one executable Aether task.
    for atom in recipe:
        mapped_task_id = atom_mapping.get(atom)
        if not mapped_task_id or mapped_task_id in existing_task_ids:
            continue
        if atom not in {"journey_cascade", "joint_inspection_plan", "shared_compliance_profile", "renewal_bundle"}:
            continue
        meta = atom_meta.get(atom) or {}
        tasks.append(
            _task(
                mapped_task_id,
                meta.get("label", atom.replace("_", " ").title()),
                atom,
                ["internal_data_normalization"],
                f"Execute or prepare the {atom} work atom.",
            )
        )
        existing_task_ids.add(mapped_task_id)

    for atom in recipe:
        mapped_task_id = atom_mapping.get(atom)
        if atom == "register_case" or (mapped_task_id and mapped_task_id in existing_task_ids):
            continue
        task_id = mapped_task_id or ("internal_work_atom_" + atom)
        if task_id in existing_task_ids:
            continue
        meta = atom_meta.get(atom) or {
            "label": atom.replace("_", " ").replace("/", " / ").title(),
            "automation": "prepare_only",
            "human_boundary": False,
        }
        operation = atom if mapped_task_id else "work_atom"
        tasks.append(
            _task(
                task_id,
                meta["label"],
                operation,
                ["internal_data_normalization"],
                f"Execute or prepare the {atom} employee work atom according to its authority mode.",
            )
        )
        existing_task_ids.add(task_id)

    # This packet is intentionally available before completion; it prepares
    # the structure a statutory decision-maker will need, without making the
    # decision itself.
    decision_deps = ["internal_case_notes", "internal_form_prep", "internal_deficiency"]
    tasks.append(
        _task(
            "internal_decision_brief",
            "Automatic statutory decision brief",
            "decision_brief",
            list(dict.fromkeys(decision_deps)),
            "Prepare evidence, contradictions, outstanding issues and rule-reference placeholders for the authorised decision-maker.",
        )
    )

    if profile.post_decision_followup:
        post_deps = list(original_ids) + [
            task.id for task in tasks
            if task.id not in {"internal_case_closeout", "internal_post_decision"}
        ]
        tasks.append(
            _task(
                "internal_post_decision",
                "Automatic post-decision execution plan",
                "post_decision",
                list(dict.fromkeys(post_deps)),
                "Prepare record-update, dispatch, compliance and renewal actions after the statutory outcome.",
            )
        )

    closeout_deps = list(original_ids) + [
        task.id for task in tasks
        if task.id != "internal_case_closeout"
    ]
    tasks.append(
        _task(
            "internal_case_closeout",
            "Automatic case-file closeout",
            "case_closeout",
            list(dict.fromkeys(closeout_deps)),
            "Assemble the final administrative case file after service work and human boundaries are complete.",
        )
    )
    return tasks
