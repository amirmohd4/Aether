"""Reusable employee-work recipes derived from Indian government process archetypes.

Recipes describe recurring administrative actions. Jurisdiction-specific legal
rules, authority matrices, forms and timelines remain separate.
"""

EMPLOYEE_WORK_ATOMS = {
    "register_case": {"label": "Register / diarize case", "automation": "full_with_connector", "human_boundary": False},
    "journey_cascade": {"label": "Prepare downstream government journey", "automation": "full", "human_boundary": False},
    "check_completeness": {"label": "Check application completeness", "automation": "full", "human_boundary": False},
    "extract_document_facts": {"label": "Extract facts from documents", "automation": "full", "human_boundary": False},
    "lookup_record": {"label": "Lookup departmental record", "automation": "full_with_connector", "human_boundary": False},
    "lookup_land_record": {"label": "Lookup land record", "automation": "full_with_connector", "human_boundary": False},
    "lookup_property_record": {"label": "Lookup property/registration record", "automation": "full_with_connector", "human_boundary": False},
    "reconcile_records": {"label": "Reconcile records", "automation": "full", "human_boundary": False},
    "prepare_deficiency": {"label": "Prepare deficiency notice", "automation": "draft_then_authorize", "human_boundary": True},
    "prepare_query": {"label": "Prepare response to official query", "automation": "draft_then_authorize", "human_boundary": True},
    "prepare_certificate": {"label": "Prepare certificate data/packet", "automation": "draft_then_authorize", "human_boundary": True},
    "prepare_order": {"label": "Prepare order/processing packet", "automation": "draft_then_authorize", "human_boundary": True},
    "prepare_decision_brief": {"label": "Prepare statutory decision brief", "automation": "draft_then_authorize", "human_boundary": True},
    "prepare_recommendation": {"label": "Prepare recommendation", "automation": "draft_then_authorize", "human_boundary": True},
    "prepare_committee_agenda": {"label": "Prepare committee agenda packet", "automation": "draft_then_authorize", "human_boundary": True},
    "prepare_inspection_packet": {"label": "Prepare inspection packet", "automation": "full", "human_boundary": False},
    "schedule_inspection": {"label": "Schedule inspection", "automation": "full_with_connector", "human_boundary": False},
    "joint_inspection_plan": {"label": "Build joint inspection plan", "automation": "full_then_authorize", "human_boundary": True},
    "shared_compliance_profile": {"label": "Build shared compliance profile", "automation": "full", "human_boundary": False},
    "renewal_bundle": {"label": "Build one-renewal compliance bundle", "automation": "full_then_authorize", "human_boundary": True},
    "schedule_field_visit": {"label": "Schedule field visit", "automation": "full_with_connector", "human_boundary": False},
    "coordinate_nocs": {"label": "Coordinate inter-department NOCs/reports", "automation": "full_with_connector", "human_boundary": False},
    "request_field_report": {"label": "Request field/verification report", "automation": "full_with_connector", "human_boundary": False},
    "calculate_duty": {"label": "Calculate stamp/registration duty", "automation": "rule_backed", "human_boundary": False},
    "calculate_fee": {"label": "Calculate applicable fee", "automation": "rule_backed", "human_boundary": False},
    "check_dues": {"label": "Check outstanding dues", "automation": "full_with_connector", "human_boundary": False},
    "reconcile_demand_payment": {"label": "Reconcile demand and payment", "automation": "full_with_connector", "human_boundary": False},
    "prepare_form": {"label": "Prepare downstream departmental form", "automation": "full_then_authorize", "human_boundary": True},
    "compare_resubmission": {"label": "Compare resubmitted evidence", "automation": "full", "human_boundary": False},
    "start_followup_watch": {"label": "Watch pending response/follow-up", "automation": "full", "human_boundary": False},
    "sla_escalation": {"label": "Escalate SLA risk", "automation": "policy_backed", "human_boundary": True},
    "prepare_dispatch": {"label": "Prepare dispatch/notification", "automation": "full_with_connector", "human_boundary": False},
    "renewal_watch": {"label": "Start renewal/compliance watch", "automation": "full", "human_boundary": False},
    "start_appeal_watch": {"label": "Track appeal/limitation window", "automation": "full", "human_boundary": False},
}
 
PROCESS_WORK_RECIPES = {
    "certificate": [
        "register_case", "check_completeness", "extract_document_facts",
        "lookup_record", "reconcile_records", "prepare_deficiency",
        "prepare_certificate", "prepare_decision_brief",
    ],
    "property_registration": [
        "register_case", "journey_cascade", "check_completeness", "extract_document_facts",
        "scrutinize_deed", "verify_identity", "lookup_encumbrance",
        "lookup_property_record", "calculate_duty", "reconcile_records",
        "schedule_appointment", "prepare_registration_packet",
        "prepare_decision_brief",
    ],
    "land_mutation": [
        "register_case", "check_completeness", "lookup_land_record",
        "prepare_notice", "request_field_report", "track_objections",
        "reconcile_records", "prepare_decision_brief", "start_appeal_watch",
    ],
    "property_record": [
        "register_case", "check_completeness", "lookup_property_record",
        "reconcile_records", "prepare_certificate", "prepare_decision_brief",
    ],
    "registration": [
        "register_case", "scrutinize_deed", "verify_identity",
        "calculate_duty", "lookup_encumbrance", "reconcile_records",
        "schedule_appointment", "prepare_registration_packet",
    ],
    "municipal_license": [
        "register_case", "journey_cascade", "check_completeness", "lookup_property",
        "zoning_scrutiny", "check_dues", "coordinate_nocs",
        "schedule_inspection", "prepare_demand", "prepare_decision_brief",
    ],
    "building_permit": [
        "register_case", "journey_cascade", "check_completeness", "plan_scrutiny",
        "lookup_property", "zoning_scrutiny", "check_dues",
        "coordinate_nocs", "schedule_inspection", "joint_inspection_plan",
        "shared_compliance_profile", "prepare_committee_agenda",
        "prepare_decision_brief",
    ],
    "fire_safety": [
        "register_case", "check_completeness", "plan_scrutiny",
        "schedule_inspection", "ingest_inspection_report",
        "prepare_recommendation", "prepare_noc",
    ],
    "factory_license": [
        "register_case", "check_completeness", "lookup_property",
        "labour_compliance", "coordinate_nocs", "schedule_inspection",
        "joint_inspection_plan", "shared_compliance_profile",
        "prepare_recommendation", "prepare_decision_brief",
    ],
    "health_regulatory": [
        "register_case", "check_completeness", "verify_professional",
        "lookup_record", "coordinate_nocs", "schedule_inspection",
        "prepare_recommendation", "prepare_decision_brief",
    ],
    "food_license": [
        "register_case", "journey_cascade", "classify_business", "check_completeness",
        "validate_premises", "schedule_inspection", "joint_inspection_plan",
        "shared_compliance_profile", "renewal_bundle", "prepare_recommendation",
        "calculate_fee", "prepare_decision_brief",
    ],
    "environment": [
        "register_case", "check_completeness", "classify_project",
        "scrutinize_technical_documents", "lookup_prior_consents",
        "coordinate_nocs", "schedule_inspection", "prepare_conditions",
        "prepare_decision_brief", "start_compliance_watch",
    ],
    "transport": [
        "register_case", "check_completeness", "verify_identity",
        "lookup_vehicle_or_driver_record", "calculate_fee",
        "schedule_appointment", "prepare_licence_packet",
    ],
    "vehicle_registration": [
        "register_case", "check_completeness", "verify_identity",
        "lookup_vehicle", "verify_insurance_and_finance",
        "calculate_fee", "schedule_inspection", "prepare_registration_packet",
    ],
    "tax": [
        "register_case", "validate_return", "lookup_tax_record",
        "detect_discrepancy", "prepare_query", "compare_response",
        "reconcile_demand_payment", "prepare_order",
    ],
    "corporate_incorporation": [
        "register_case", "journey_cascade", "check_completeness",
        "validate_entity", "prepare_form", "compare_resubmission",
        "reconcile_registry_records", "shared_compliance_profile",
        "prepare_certificate", "prepare_decision_brief",
    ],
    "corporate": [
        "register_case", "check_completeness", "validate_entity",
        "prepare_form", "compare_resubmission", "reconcile_registry_records",
        "prepare_certificate",
    ],
    "benefit": [
        "register_case", "check_completeness", "verify_identity",
        "check_eligibility", "duplicate_check", "verify_beneficiary",
        "prepare_sanction_packet", "reconcile_payment", "renewal_watch",
    ],
    "police": [
        "register_case", "verify_identity", "lookup_case_record",
        "request_field_verification", "prepare_report",
        "prepare_response", "start_followup_watch",
    ],
    "passport": [
        "register_case", "check_completeness", "verify_identity",
        "schedule_appointment", "coordinate_police_verification",
        "review_adverse_report", "prepare_dispatch",
    ],
    "adjudication": [
        "register_case", "check_limitation", "assemble_record",
        "issue_notice", "prepare_hearing_packet", "prepare_brief",
        "track_order", "start_appeal_watch",
    ],
    "grievance": [
        "register_case", "classify_grievance", "route_case",
        "assemble_evidence", "prepare_response", "sla_escalation",
        "close_case",
    ],
    "information_access": [
        "register_case", "jurisdiction_check", "route_to_cpio",
        "assemble_records", "prepare_response", "appeal_watch",
    ],
    "procurement": [
        "register_case", "prepare_tender_file", "scrutinize_bids",
        "consolidate_clarifications", "prepare_comparative_statement",
        "prepare_committee_agenda", "track_award", "contract_monitoring",
    ],
    "utility_connection": [
        "register_case", "check_completeness", "verify_property",
        "calculate_demand", "schedule_field_visit",
        "prepare_connection_order", "reconcile_payment",
    ],
    "rural_development": [
        "register_case", "check_completeness", "verify_household_or_land",
        "prepare_field_verification_packet", "check_eligibility",
        "prepare_sanction_packet", "reconcile_payment",
    ],
    "employment": [
        "register_case", "check_completeness", "verify_eligibility",
        "route_to_training_or_employer", "track_response", "prepare_outcome",
    ],
}

ATOM_TASK_MAPPING = {
    "register_case": "engine_case_creation",
    "journey_cascade": "internal_journey_cascade",
    "check_completeness": "internal_case_file",
    "extract_document_facts": "document_intake",
    "lookup_record": "service_lookup",
    "lookup_land_record": "land_record",
    "lookup_property_record": "registration_record",
    "reconcile_records": "cross_record_reconciliation",
    "prepare_deficiency": "internal_deficiency",
    "prepare_query": "internal_query_response",
    "prepare_certificate": "internal_post_decision",
    "prepare_order": "internal_decision_brief",
    "prepare_decision_brief": "internal_decision_brief",
    "prepare_recommendation": "internal_decision_brief",
    "prepare_committee_agenda": "internal_decision_brief",
    "prepare_inspection_packet": "internal_inspection_packet",
    "schedule_inspection": "internal_inspection_packet",
    "joint_inspection_plan": "internal_joint_inspection",
    "shared_compliance_profile": "internal_shared_compliance_profile",
    "renewal_bundle": "internal_renewal_bundle",
    "schedule_field_visit": "internal_inspection_packet",
    "coordinate_nocs": "internal_interdepartment_handoff",
    "request_field_report": "internal_interdepartment_handoff",
    "calculate_duty": "internal_fee_reconciliation",
    "calculate_fee": "internal_fee_reconciliation",
    "check_dues": "internal_fee_reconciliation",
    "reconcile_demand_payment": "internal_fee_reconciliation",
    "prepare_form": "internal_form_prep",
    "compare_resubmission": "internal_data_normalization",
    "start_followup_watch": "internal_followup_plan",
    "sla_escalation": "internal_sla_snapshot",
    "prepare_dispatch": "internal_post_decision",
    "renewal_watch": "internal_post_decision",
    "start_appeal_watch": "internal_followup_plan",
}
 

def atom_task_mapping() -> dict[str, str]:
    return dict(ATOM_TASK_MAPPING)


def work_atom_metadata() -> dict[str, dict[str, object]]:
    return dict(EMPLOYEE_WORK_ATOMS)


def work_recipe(process_key: str) -> list[str]:
    return list(PROCESS_WORK_RECIPES.get(process_key, (
        "register_case",
        "check_completeness",
        "extract_document_facts",
        "lookup_record",
        "reconcile_records",
        "prepare_decision_brief",
    )))
