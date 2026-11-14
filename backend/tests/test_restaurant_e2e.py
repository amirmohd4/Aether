from aether_core.engine import AetherExecutionEngine
from aether_core.domain import TaskStatus


def test_restaurant_full_vertical_slice_resumes_after_inspection_and_approval():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        inputs={
            "owner_name": "Demo Owner",
            "parcel_id": "P-001",
            "area": 2.0,
            "documents": ["identity_document", "lease_or_ownership", "floor_plan"],
        },
    )

    case = engine.execute_until_pause(case.case_id)
    assert case.status == "waiting_for_human"
    assert case.tasks["inspection"].status == TaskStatus.HUMAN_REVIEW
    assert case.tasks["final_approval"].status == TaskStatus.PENDING

    # Physical inspection is completed by an authorised human/field process.
    case = engine.complete_human_task(case.case_id, "inspection", "approved", "Inspection passed")
    assert case.tasks["inspection"].status == TaskStatus.COMPLETED
    assert case.tasks["final_approval"].status == TaskStatus.HUMAN_REVIEW

    # Only statutory final authority remains human; Aether resumes automatically afterwards.
    case = engine.complete_human_task(case.case_id, "final_approval", "approved", "Approved by authorised officer")

    assert case.status == "completed"
    assert case.tasks["record_update"].status == TaskStatus.COMPLETED
    assert case.tasks["certificate"].status == TaskStatus.COMPLETED
    assert case.outcome["status"] == "completed"

def test_missing_required_documents_stop_before_downstream_execution():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        inputs={
            "owner_name": "Synthetic Missing-Docs Applicant",
            "parcel_id": "P-MISSING-DOCS",
            "area": 2.0,
            "documents": ["identity_document"],
            "enforce_intake_gate": True,
        },
    )

    paused = engine.execute_until_pause(case.case_id)

    assert paused.status == "waiting_for_human"
    assert paused.tasks["document_intake"].status == TaskStatus.HUMAN_REVIEW
    assert paused.tasks["premises_check"].status != TaskStatus.COMPLETED
    assert paused.tasks["certificate"].status != TaskStatus.COMPLETED
    assert any(
        exception.get("type") == "DOC-MISSING"
        for exception in paused.exceptions
    )

