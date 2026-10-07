from aether_core.dependency_engine import DependencyEngine
from aether_core.domain import TaskDefinition, TaskState, TaskStatus
from aether_core.engine import AetherExecutionEngine


def test_human_wait_does_not_mark_downstream_as_failed():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": [
            "identity_document", "lease_or_ownership", "business_registration",
            "food_business_details", "site_plan", "building_plan", "floor_plan",
            "fire_safety_details", "legal_occupancy", "parking_plan",
            "premises_photo", "rent_deed_or_affidavit", "employer_photo", "tax_details",
        ]},
    )
    case.tasks["human_gate"] = TaskState(TaskDefinition(
        "human_gate", "Physical verification", "Authority", "InspectionCoordinator",
        physical_action=True,
    ))
    case.tasks["after_gate"] = TaskState(TaskDefinition(
        "after_gate", "Post-verification check", "Aether", "DigitalWorker", ["human_gate"],
    ))

    case = engine.execute_until_pause(case.case_id)

    assert case.tasks["human_gate"].status == TaskStatus.HUMAN_REVIEW
    assert case.tasks["after_gate"].status == TaskStatus.PENDING


def test_independent_work_continues_while_human_branch_waits():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={},
    )
    case.tasks["human_gate"] = TaskState(TaskDefinition(
        "human_gate", "Physical verification", "Authority", "InspectionCoordinator",
        physical_action=True,
    ))
    case.tasks["independent_check"] = TaskState(TaskDefinition(
        "independent_check", "Independent digital check", "Aether", "DigitalWorker",
    ))

    case = engine.execute_until_pause(case.case_id)

    assert case.tasks["human_gate"].status == TaskStatus.HUMAN_REVIEW
    assert case.tasks["independent_check"].status == TaskStatus.COMPLETED
    assert case.status == "waiting_for_human"


def test_dependency_engine_distinguishes_waiting_from_failure():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={},
    )
    snapshot = DependencyEngine().refresh(case)
    assert "identity_check" in snapshot.ready
    assert snapshot.blocked == []
