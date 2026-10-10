from __future__ import annotations

from typing import Any, Dict


BASELINE_MINUTES = {
    "register_case": 4,
    "check_completeness": 6,
    "extract_document_facts": 10,
    "lookup_record": 7,
    "lookup_land_record": 8,
    "lookup_property_record": 8,
    "reconcile_records": 12,
    "prepare_deficiency": 8,
    "prepare_query": 8,
    "prepare_certificate": 6,
    "prepare_order": 8,
    "prepare_decision_brief": 15,
    "prepare_recommendation": 12,
    "prepare_form": 10,
    "coordinate_nocs": 12,
    "request_field_report": 6,
    "schedule_inspection": 5,
    "joint_inspection_plan": 10,
    "shared_compliance_profile": 12,
    "renewal_bundle": 12,
    "intermediate_handoff_tracking": 8,
    "verification_chain_tracking": 10,
    "service_center_packet": 10,
    "claim_query_tracking": 8,
    "nodal_route": 8,
    "claim_anomaly_screen": 10,
    "multi_level_verification": 10,
    "dbt_readiness": 6,
    "retirement_preflight": 15,
    "case_passport": 8,
    "preflight_check": 8,
    "duplicate_case_screen": 7,
    "authoritative_prefill": 10,
    "deadline_guard": 4,
    "resubmission_diff_packet": 12,
    "whole_government_route": 10,
    "journey_cascade": 6,
    "journey_bundle": 12,
    "continuity_review": 8,
    "inspection_quality_guard": 7,
}


def estimate_effort_impact(process: Dict[str, Any], completed_atoms: set[str] | None = None) -> Dict[str, Any]:
    recipe = list(process.get("employee_work_recipe") or [])
    completed = completed_atoms or set()

    estimated_employee_minutes = sum(BASELINE_MINUTES.get(atom, 5) for atom in recipe if atom in completed or not completed)
    aether_minutes = max(1, len(recipe))
    employee_minutes_saved = max(0, estimated_employee_minutes - aether_minutes)

    forms_prepared = sum(
        1 for atom in recipe if atom in {"prepare_form", "resubmission_diff_packet", "service_center_packet"}
    )
    lookups = sum(
        1 for atom in recipe if "lookup" in atom or atom in {"authoritative_prefill", "continuity_review"}
    )
    coordination = sum(
        1 for atom in recipe if atom in {
            "coordinate_nocs",
            "whole_government_route",
            "nodal_route",
            "intermediate_handoff_tracking",
            "verification_chain_tracking",
        }
    )
    document_work = sum(
        1 for atom in recipe if atom in {"check_completeness", "extract_document_facts", "prepare_deficiency"}
    )

    physical = len(process.get("human_boundary") or [])
    user_reentry_avoided = max(0, forms_prepared - 1)
    followup_chases_avoided = coordination + sum(
        1 for atom in recipe if atom in {"deadline_guard", "start_followup_watch", "sla_escalation"}
    )
    duplicate_entry_avoided = forms_prepared + lookups

    return {
        "employee": {
            "estimated_manual_minutes": estimated_employee_minutes,
            "estimated_aether_minutes": aether_minutes,
            "estimated_minutes_saved": employee_minutes_saved,
            "form_preparation_steps_automated": forms_prepared,
            "record_lookups_automated": lookups,
            "coordination_steps_automated": coordination,
            "document_steps_automated": document_work,
        },
        "citizen_or_business": {
            "duplicate_reentry_steps_avoided": duplicate_entry_avoided,
            "form_reentry_steps_avoided": user_reentry_avoided,
            "followup_chases_avoided": followup_chases_avoided,
            "physical_or_statutory_wait_points_remaining": physical,
            "one_journey_experience": True,
        },
        "measurement_policy": {
            "is_telemetry": False,
            "purpose": "planning and pilot KPI baseline",
            "replace_with_observed_time": True,
        },
    }
