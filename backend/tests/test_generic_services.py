from aether_core.engine import AetherExecutionEngine
from aether_core.domain import TaskStatus


def test_non_specialized_service_uses_generic_process_instead_of_project_process():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want a driving license",
        customer_type="citizen",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={},
    )
    assert case.service_id == "driving_license"
    task_ids = set(case.tasks)
    assert "department_processing" in task_ids
    assert "building" not in task_ids
    assert "rera" not in task_ids

    case = engine.execute_until_pause(case.case_id)
    assert case.tasks["department_processing"].status == TaskStatus.COMPLETED
    assert case.tasks["final_approval"].status == TaskStatus.HUMAN_REVIEW


def test_human_approval_resumes_generic_service_to_outcome():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to register a company",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={},
    )
    case = engine.execute_until_pause(case.case_id)
    assert case.status == "waiting_for_human"
    case = engine.complete_human_task(case.case_id, "final_approval", "approved", "demo authority")
    assert case.status == "completed"
    assert case.outcome["service_outcome"] == "company_registration"


def test_human_decision_audit_records_actor_identity():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to register a company",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={},
        owner_user_id="user-audit",
        tenant_id="tenant-audit",
    )
    case = engine.execute_until_pause(case.case_id)
    case = engine.complete_human_task(
        case.case_id,
        "final_approval",
        "approved",
        "approved by officer",
        actor_id="officer-42",
        actor_role="officer",
    )
    matching = [
        event for event in case.execution_events
        if event.get("action") == "human_action.approved"
    ]
    assert matching
    assert matching[-1]["actor"] == "officer-42"
