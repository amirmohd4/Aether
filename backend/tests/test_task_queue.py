from datetime import datetime, timedelta

from aether_core.task_queue import DurableTaskQueue


def test_queue_claim_and_complete_round_trip():
    queue = DurableTaskQueue(lease_seconds=60)
    row = queue.enqueue("queue-test-case", "task-a", {"value": 1})
    claim = queue.claim("queue-test-case")

    assert claim is not None
    assert claim.queue_id == row.id
    assert claim.case_id == "queue-test-case"
    assert claim.task_id == "task-a"
    assert claim.attempts == 1

    queue.complete(claim.queue_id)
    item = [x for x in queue.for_case("queue-test-case") if x["task_id"] == "task-a"][0]
    assert item["status"] == queue.COMPLETED
    assert item["locked_by"] is None


def test_queue_reclaims_expired_lease():
    queue = DurableTaskQueue(lease_seconds=60)
    queue.enqueue("queue-recovery-case", "task-a", {})
    claim = queue.claim("queue-recovery-case")
    assert claim is not None

    # Force the lease into the past through the repository model so the
    # recovery path can be tested deterministically without sleeping.
    from backend.database import SessionLocal
    from aether_core.persistence_models import AetherTaskQueueRecord

    with SessionLocal() as db:
        row = db.get(AetherTaskQueueRecord, claim.queue_id)
        row.lease_until = datetime.utcnow() - timedelta(seconds=1)
        db.commit()

    assert queue.reclaim_expired("queue-recovery-case") == 1
    reclaimed = queue.claim("queue-recovery-case")
    assert reclaimed is not None
    assert reclaimed.task_id == "task-a"
    assert reclaimed.attempts == 2


def test_usage_metering_is_idempotent_for_case_event():
    from aether_core.case_store import DatabaseCaseStore

    store = DatabaseCaseStore()
    first = store.record_usage(
        tenant_id="meter-tenant",
        case_id="meter-case-001",
        customer_type="bank",
        event_type="case_completed",
        unit_type="outcome",
        units=1,
    )
    second = store.record_usage(
        tenant_id="meter-tenant",
        case_id="meter-case-001",
        customer_type="bank",
        event_type="case_completed",
        unit_type="outcome",
        units=1,
    )

    assert first["id"] == second["id"]
    usage = store.usage_summary("meter-tenant", event_type="case_completed")
    assert usage["usage"][0]["units"] == 1
