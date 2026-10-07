from aether_core.case_store import DatabaseCaseStore
from aether_core.engine import AetherExecutionEngine
from aether_core.domain import TaskStatus


def test_case_survives_a_new_engine_instance():
    first_engine = AetherExecutionEngine()
    case = first_engine.create_case(
        objective="Verify this property for a bank loan",
        customer_type="bank",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"property_id": "P-DURABLE-001"},
    )
    first_engine.execute_until_pause(case.case_id)

    second_engine = AetherExecutionEngine()
    recovered = second_engine.get_case(case.case_id)

    assert recovered.case_id == case.case_id
    assert recovered.objective == case.objective
    assert recovered.service_id == case.service_id
    assert "tasks" in DatabaseCaseStore._serialize_case(recovered)
    assert second_engine.store.events_for(case.case_id)


def test_event_store_preserves_order():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="Verify this property for a bank loan",
        customer_type="bank",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={},
    )
    engine.execute_until_pause(case.case_id)
    events = engine.store.events_for(case.case_id)

    assert events
    assert [event["sequence"] for event in events] == sorted(event["sequence"] for event in events)



def test_task_checkpoint_survives_case_reload_without_a_fresh_case_blob():
    first_engine = AetherExecutionEngine()
    case = first_engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"property_id": "P-CHECKPOINT-001"},
    )

    task = case.tasks["document_intake"]
    task.status = TaskStatus.RUNNING
    task.attempts = 1
    task.idempotency_key = f"{case.case_id}:document_intake"
    task.result = {"checkpoint": "durable"}
    first_engine.store.put_task_checkpoint(case.case_id, task)

    second_engine = AetherExecutionEngine()
    recovered = second_engine.get_case(case.case_id)

    recovered_task = recovered.tasks["document_intake"]
    assert recovered_task.status == TaskStatus.RUNNING
    assert recovered_task.attempts == 1
    assert recovered_task.result == {"checkpoint": "durable"}
    assert recovered_task.idempotency_key == f"{case.case_id}:document_intake"
