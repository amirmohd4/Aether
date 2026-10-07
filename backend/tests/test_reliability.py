from aether_core.connectors import SyntheticConnector
from aether_core.engine import AetherExecutionEngine
from aether_core.domain import TaskStatus


def test_synthetic_connector_reuses_request_for_same_idempotency_key():
    connector = SyntheticConnector("Revenue")
    first = connector.submit("land_record", {"parcel_id": "P-001"}, "case-1:land_record")
    second = connector.submit("land_record", {"parcel_id": "P-001"}, "case-1:land_record")
    assert first["request_id"] == second["request_id"]


def test_task_execution_retries_and_keeps_stable_idempotency_key():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="Verify this property for a bank loan",
        customer_type="bank",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={},
    )

    class FlakyWorker:
        def __init__(self):
            self.calls = 0
        def execute(self, context):
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("transient failure")
            return {
                "request_id": "REQ-RETRY",
                "status": "completed",
                "result": {"source": "Synthetic"},
            }

    worker = FlakyWorker()
    engine.workers._workers["DocumentWorker"] = worker
    task = case.tasks["document_intake"]
    case = engine.execute_until_pause(case.case_id)

    assert task.status == TaskStatus.COMPLETED
    assert task.attempts == 2
    assert task.idempotency_key == f"{case.case_id}:document_intake"
    assert any(e["action"] == "task.failed_attempt" for e in case.execution_events)
    assert any(e["action"] == "task.completed" for e in case.execution_events)
    assert engine.audit.for_case(case.case_id)


def test_case_summary_includes_execution_events():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="Verify this property for a bank loan",
        customer_type="bank",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={},
    )
    case = engine.execute_until_pause(case.case_id)
    summary = case.summary()
    assert "execution_events" in summary
    assert summary["execution_events"]
