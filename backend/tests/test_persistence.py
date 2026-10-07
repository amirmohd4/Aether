from aether_core.case_store import DatabaseCaseStore
from aether_core.engine import AetherExecutionEngine


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
