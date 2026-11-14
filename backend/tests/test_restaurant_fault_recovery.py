from aether_core.engine import AetherExecutionEngine
from aether_core.domain import TaskStatus


JURISDICTION = {
    "country": "India",
    "state": "Jammu and Kashmir",
    "district": "Jammu",
}
DOCUMENTS = ["identity_document", "lease_or_ownership", "floor_plan"]


def create_restaurant_case(**extra_inputs):
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction=JURISDICTION,
        inputs={
            "owner_name": "Synthetic Test Applicant",
            "parcel_id": "P-FAULT-001",
            "area": 2.0,
            "documents": DOCUMENTS,
            **extra_inputs,
        },
    )
    return engine, case


def test_transient_failures_retry_and_workflow_can_finish():
    engine, case = create_restaurant_case(simulate_failure_once=True)

    paused = engine.execute_until_pause(case.case_id)
    assert paused.status == "waiting_for_human"
    assert paused.tasks["identity_check"].status == TaskStatus.COMPLETED
    assert paused.tasks["identity_check"].attempts == 2

    after_inspection = engine.complete_human_task(
        case.case_id, "inspection", "approved", "Synthetic inspection passed"
    )
    assert after_inspection.status == "waiting_for_human"
    assert after_inspection.tasks["final_approval"].status == TaskStatus.HUMAN_REVIEW

    completed = engine.complete_human_task(
        case.case_id, "final_approval", "approved", "Synthetic authorised approval"
    )
    assert completed.status == "completed"
    assert all(task.status == TaskStatus.COMPLETED for task in completed.tasks.values())
    assert completed.tasks["certificate"].result["completed"] is True
    assert completed.tasks["certificate"].result["source"] == "Aether Outcome Engine"


def test_rejected_statutory_approval_never_issues_certificate():
    engine, case = create_restaurant_case()

    paused = engine.execute_until_pause(case.case_id)
    assert paused.status == "waiting_for_human"

    after_inspection = engine.complete_human_task(
        case.case_id, "inspection", "approved", "Synthetic inspection passed"
    )
    assert after_inspection.tasks["final_approval"].status == TaskStatus.HUMAN_REVIEW

    rejected = engine.complete_human_task(
        case.case_id, "final_approval", "rejected", "Synthetic statutory rejection"
    )
    assert rejected.status == "exception"
    assert rejected.tasks["final_approval"].status == TaskStatus.EXCEPTION
    assert rejected.tasks["record_update"].status != TaskStatus.COMPLETED
    assert rejected.tasks["certificate"].status != TaskStatus.COMPLETED
    assert rejected.outcome is None
