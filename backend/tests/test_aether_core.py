from aether_core.engine import AetherExecutionEngine
from aether_core.domain import TaskStatus


def test_restaurant_case_runs_parallel_work_until_human_boundary():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir", "district": "Demo District"},
        inputs={"owner_name": "Demo Owner", "parcel_id": "P-001", "area": 2.0},
    )
    case = engine.execute_until_pause(case.case_id)

    assert case.status == "waiting_for_human", {
        "exceptions": case.exceptions,
        "non_completed": {
            key: {
                "status": state.status.value,
                "error": state.error,
                "operation": state.definition.operation,
            }
            for key, state in case.tasks.items()
            if state.status.value != "completed"
        },
    }
    assert case.tasks["identity_check"].status == TaskStatus.COMPLETED
    assert case.tasks["food_review"].status == TaskStatus.COMPLETED
    assert case.tasks["fire_review"].status == TaskStatus.COMPLETED
    assert case.tasks["inspection"].status == TaskStatus.HUMAN_REVIEW
    assert case.tasks["final_approval"].status in {TaskStatus.PENDING, TaskStatus.BLOCKED}


def test_property_conflict_creates_exception_and_human_review():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="Verify this property for a bank loan",
        customer_type="bank",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={
            "owner_name": "Demo Owner",
            "parcel_id": "P-001",
            "area": 2.0,
            "registration_area": 2.08,
            "simulate_conflict": True,
        },
    )
    case = engine.execute_until_pause(case.case_id)

    assert any(e.get("type") == "record_conflict" for e in case.exceptions)
    assert case.tasks["legal_review"].status == TaskStatus.HUMAN_REVIEW
    assert case.tasks["court_search"].status == TaskStatus.COMPLETED
    assert case.tasks["tax_dues"].status == TaskStatus.COMPLETED
