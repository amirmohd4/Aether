from __future__ import annotations

from typing import Any, Dict

"""India government process playbook.

This is an operational archetype layer. It intentionally does not assert that
the same legal steps or timelines apply in every State/UT/local body. Exact
jurisdiction profiles must override it before production execution.
"""

INDIA_PROCESS_PLAYBOOK = {
    "certificate": {
        "stages": ["submission", "diarisation", "completeness", "record_verification", "deficiency_if_needed", "approval", "issuance"],
        "employee_work": ["register", "check_documents", "lookup_records", "reconcile", "draft_deficiency", "prepare_issuance"],
        "parallelizable": ["record_verification", "identity_check", "document_validation"],
        "citizen_wait_points": ["deficiency", "statutory_approval"],
        "human_boundary": ["statutory_approval"],
    },
    "property_registration": {
        "stages": ["draft/check_deed", "identity_ekyc", "duty_fee", "appointment_or_presence", "registration", "record_update", "mutation"],
        "employee_work": ["scrutinise_deed", "validate_parties", "calculate_duty", "verify_restrictions", "register_record", "trigger_downstream_updates"],
        "parallelizable": ["identity_ekyc", "record_restriction_check", "fee_calculation"],
        "citizen_wait_points": ["appointment_or_presence", "exception_resolution"],
        "human_boundary": ["statutory_registration"],
    },
    "land_mutation": {
        "stages": ["application", "record_lookup", "notice", "objection_window", "field_verification", "order", "record_update"],
        "employee_work": ["record_lookup", "notice_generation", "objection_tracking", "field_packet", "reconciliation", "order_packet"],
        "parallelizable": ["record_lookup", "document_validation", "tax_due_check"],
        "citizen_wait_points": ["notice_objection", "field_verification", "order"],
        "human_boundary": ["field_verification", "statutory_order"],
    },
    "municipal_license": {
        "stages": ["submission", "document_scrutiny", "property_zoning", "dues", "NOCs", "inspection", "demand", "decision", "renewal"],
        "employee_work": ["diarise", "scrutinise", "map_property", "coordinate_NOCs", "inspection_packet", "demand", "decision_brief", "renewal_watch"],
        "parallelizable": ["zoning", "dues", "NOCs", "document_scrutiny"],
        "citizen_wait_points": ["inspection", "deficiency", "decision"],
        "human_boundary": ["inspection", "statutory_decision"],
    },
    "building_permit": {
        "stages": ["submission", "plan_scrutiny", "land_record", "zoning", "utilities", "fire", "joint_inspection", "committee_or_authority_decision", "fee", "permit"],
        "employee_work": ["plan_scrutiny", "cross_record_check", "NOC_coordination", "joint_inspection_packet", "committee_agenda", "fee_reconciliation", "decision_brief"],
        "parallelizable": ["zoning", "fire", "utilities", "land_record"],
        "citizen_wait_points": ["inspection", "authority_decision"],
        "human_boundary": ["inspection", "statutory_decision"],
    },
    "food_license": {
        "stages": ["submission", "premises_validation", "document_scrutiny", "risk_classification", "inspection", "decision", "renewal"],
        "employee_work": ["classify_business", "validate_premises", "scrutinise_docs", "inspection_packet", "recommendation", "renewal_bundle"],
        "parallelizable": ["document_scrutiny", "business_classification", "record_checks"],
        "citizen_wait_points": ["inspection", "deficiency", "decision"],
        "human_boundary": ["inspection", "statutory_decision"],
    },
    "factory_license": {
        "stages": ["submission", "factory_plan_scrutiny", "labour_checks", "NOCs", "risk_assessment", "inspection", "licence"],
        "employee_work": ["plan_scrutiny", "labour_compliance", "NOC_coordination", "risk_pack", "inspection_packet", "recommendation"],
        "parallelizable": ["labour_checks", "document_scrutiny", "NOCs"],
        "citizen_wait_points": ["inspection", "decision"],
        "human_boundary": ["inspection", "statutory_decision"],
    },
    "environment": {
        "stages": ["project_classification", "document_screening", "prior_consent_lookup", "interdepartmental_consults", "technical_review", "inspection_or_site_review", "conditions", "decision"],
        "employee_work": ["classify_project", "screen_documents", "lookup_prior_orders", "coordinate_consults", "prepare_conditions", "decision_brief"],
        "parallelizable": ["document_screening", "prior_record_lookup", "department_consults"],
        "citizen_wait_points": ["consultation", "site_review", "decision"],
        "human_boundary": ["technical/statutory decision"],
    },
    "tax": {
        "stages": ["filing", "system_validation", "risk/discrepancy_detection", "query", "response", "reconciliation", "order/refund"],
        "employee_work": ["validate_return", "match_records", "detect_discrepancy", "prepare_query", "compare_response", "reconcile_payment", "order_packet"],
        "parallelizable": ["return_validation", "record_matching", "payment_reconciliation"],
        "citizen_wait_points": ["query", "assessment/order"],
        "human_boundary": ["statutory assessment/order"],
    },
    "corporate": {
        "stages": ["name/entity validation", "form_submission", "pre_scrutiny", "CRC_review", "resubmission_if_needed", "certificate", "post_registration"],
        "employee_work": ["validate_entity", "pre_scrutiny", "version_submission", "prepare_resubmission", "regenerate_linked_forms", "certificate_packet"],
        "parallelizable": ["identity_checks", "PAN/TAN validation", "form consistency"],
        "citizen_wait_points": ["resubmission", "approval"],
        "human_boundary": ["registry approval"],
    },
    "benefit": {
        "stages": ["application", "identity", "eligibility", "duplicate_check", "field_verification_if_needed", "sanction", "payment", "renewal"],
        "employee_work": ["eligibility_check", "duplicate_check", "beneficiary_verification", "sanction_packet", "payment_reconciliation"],
        "parallelizable": ["identity", "eligibility", "duplicate_check", "prior_benefit_lookup"],
        "citizen_wait_points": ["field_verification", "sanction", "payment"],
        "human_boundary": ["sanction where prescribed"],
    },
    "passport": {
        "stages": ["application", "document_check", "biometrics/presence", "police_verification", "adverse_report_review_if_any", "decision", "printing", "dispatch"],
        "employee_work": ["document_advisor", "appointment", "verification_chain_tracking", "adverse_report_review_packet", "dispatch"],
        "parallelizable": ["document_validation", "eligibility_checks"],
        "citizen_wait_points": ["PSK/POPSK presence", "police verification"],
        "human_boundary": ["identity/decision and police verification as prescribed"],
    },
    "police": {
        "stages": ["complaint/verification request", "registration", "record lookup", "field/station verification", "report", "communication"],
        "employee_work": ["diary/register", "record lookup", "route", "field packet", "report draft", "status communication"],
        "parallelizable": ["record lookup", "identity validation"],
        "citizen_wait_points": ["field verification", "officer review"],
        "human_boundary": ["police finding/report"],
    },
    "adjudication": {
        "stages": ["filing", "jurisdiction/limitation", "record assembly", "notice", "reply", "hearing", "order", "appeal"],
        "employee_work": ["registry", "record compilation", "notice generation", "hearing bundle", "case brief", "order tracking"],
        "parallelizable": ["record collection", "limitation checks"],
        "citizen_wait_points": ["reply", "hearing", "order"],
        "human_boundary": ["adjudicatory decision"],
    },
    "grievance": {
        "stages": ["lodging", "classification", "routing", "evidence_request", "department_action", "response", "review/appeal"],
        "employee_work": ["classify", "route", "transfer", "request evidence", "follow up", "draft response", "review"],
        "parallelizable": ["evidence collection", "record lookup"],
        "citizen_wait_points": ["missing evidence", "department action"],
        "human_boundary": ["official resolution"],
    },
    "customs": {
        "stages": ["filing", "validation", "assessment/risk", "query", "response", "examination_if_selected", "release/order", "refund/incentive"],
        "employee_work": ["data mapping", "document verification", "query preparation", "response comparison", "examination packet", "release/reconciliation"],
        "parallelizable": ["document checks", "record matching", "risk checks"],
        "citizen_wait_points": ["query", "physical examination if selected"],
        "human_boundary": ["customs assessment/examination decisions"],
    },
    "utility_connection": {
        "stages": ["application", "document/property check", "technical feasibility", "demand", "site visit", "connection order", "payment"],
        "employee_work": ["validate", "property lookup", "technical checklist", "demand calculation", "field packet", "connection order"],
        "parallelizable": ["document/property checks", "dues", "technical checks"],
        "citizen_wait_points": ["site visit", "payment"],
        "human_boundary": ["field decision where prescribed"],
    },
    "pension": {
        "stages": ["pre-retirement preparation", "service record validation", "nomination/family verification", "dues/leave reconciliation", "sanction", "PPO", "payment", "grievance"],
        "employee_work": ["record reconciliation", "missing-document chase", "family/nomination verification", "dues reconciliation", "sanction packet", "PPO tracking"],
        "parallelizable": ["service record checks", "nomination checks", "bank details", "dues"],
        "citizen_wait_points": ["missing record", "sanction"],
        "human_boundary": ["sanction/authorised certification"],
    },
}


GENERIC_PROCESS_PLAYBOOK: Dict[str, Any] = {
    "stages": [
        "submission",
        "case_registration",
        "identity_and_eligibility",
        "document_scrutiny",
        "department_record_checks",
        "cross_record_reconciliation",
        "deficiency_or_query_if_needed",
        "authorised_human_decision",
        "post_decision_record_update",
        "outcome_and_follow_up",
    ],
    "employee_work": [
        "diarise",
        "classify_service_and_jurisdiction",
        "validate_evidence",
        "route_department_checks",
        "reconcile_responses",
        "prepare_deficiency_or_query",
        "assemble_decision_packet",
        "track_authorised_decision",
        "verify_post_decision_completion",
    ],
    "parallelizable": [
        "identity_and_eligibility",
        "document_validation",
        "independent_department_record_checks",
    ],
    "citizen_wait_points": [
        "missing_evidence_or_query",
        "physical_or_in_person_action_if_required",
        "authorised_decision",
    ],
    "human_boundary": [
        "statutory_or_discretionary_decision_by_competent_authority",
        "physical_action_if_required",
    ],
    "coverage": "generic_operational_archetype",
    "disclaimer": "Generic execution pattern only. It is not a service-specific statutory sequence or official checklist; resolve applicable steps from a verified jurisdiction rule pack.",
}


MULTI_DEPARTMENT_PROCESS_PLAYBOOK: Dict[str, Any] = {
    "stages": [
        "submission",
        "case_registration_and_routing",
        "lead_department_scrutiny",
        "parallel_contributor_department_checks",
        "dependency_and_response_tracking",
        "cross_department_reconciliation",
        "consolidated_deficiency_or_query_if_needed",
        "lead_authority_decision",
        "post_decision_handoffs",
        "outcome_and_follow_up",
    ],
    "employee_work": [
        "assign_lead_department",
        "create_department_work_packets",
        "dispatch_parallel_checks",
        "track_sla_and_dependencies",
        "reconcile_conflicting_responses",
        "prepare_consolidated_query",
        "assemble_decision_brief",
        "track_authority_decision",
        "confirm_downstream_handoffs",
    ],
    "parallelizable": [
        "identity_and_document_validation",
        "independent_department_checks",
        "technical_and_record_checks",
    ],
    "citizen_wait_points": [
        "consolidated_deficiency_or_query",
        "inspection_or_field_action_if_required",
        "lead_authority_decision",
    ],
    "human_boundary": [
        "statutory_decision_by_competent_lead_authority",
        "physical_action_if_required",
    ],
    "coverage": "multi_department_operational_archetype",
    "disclaimer": "Cross-department operating pattern only. Department participation, dependencies and legal sequence must be confirmed by a verified jurisdiction rule pack.",
}


def playbook_for(process_key: str) -> Dict[str, Any]:
    if process_key == "multi_department":
        return dict(MULTI_DEPARTMENT_PROCESS_PLAYBOOK)
    if process_key in INDIA_PROCESS_PLAYBOOK:
        return dict(INDIA_PROCESS_PLAYBOOK[process_key])
    return dict(GENERIC_PROCESS_PLAYBOOK)
