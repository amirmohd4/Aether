from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from backend.database import SessionLocal
from backend.aether_core.admin_action_queue import AdminActionQueue
from backend.aether_core.case_store import DatabaseCaseStore
from backend.aether_core.persistence_models import AetherAdminActionRecord


def _action(requires_human_decision=True):
    return {
        "action_type": "request_permit_receipt_or_certificate",
        "priority": "normal",
        "requires_human_decision": requires_human_decision,
        "idempotency_key": "idem-" + uuid4().hex,
        "title": "Request permit evidence",
        "required_evidence": ["permit_receipt"],
    }


def test_admin_action_requires_second_person_and_dispatch_is_verified():
    DatabaseCaseStore().ensure_schema()
    queue = AdminActionQueue()
    tenant = "test-" + uuid4().hex
    case_id = "case-" + uuid4().hex
    action = _action()
    try:
        first = queue.enqueue(
            tenant_id=tenant, case_id=case_id, action=action, requested_by="requester"
        )
        duplicate = queue.enqueue(
            tenant_id=tenant, case_id=case_id, action=action, requested_by="requester"
        )
        assert first["action_id"] == duplicate["action_id"]
        assert first["status"] == "awaiting_approval"

        with pytest.raises(ValueError, match="different authorized reviewer"):
            queue.approve(action_id=first["action_id"], tenant_id=tenant, approver="requester")

        approved = queue.approve(
            action_id=first["action_id"], tenant_id=tenant, approver="reviewer"
        )
        assert approved["status"] == "queued"
        assert approved["approved_by"] == "reviewer"

        result = queue.dispatch(limit=10)
        assert result["dispatched"] == 1
        saved = queue.get(action_id=first["action_id"], tenant_id=tenant)
        assert saved["status"] == "dispatched"
        assert saved["outcome"]["verified"] is True
        assert saved["outcome"]["external_effect"] is False
        assert saved["verified_at"] is not None
    finally:
        with SessionLocal() as db:
            db.query(AetherAdminActionRecord).filter_by(tenant_id=tenant).delete()
            db.commit()


def test_non_sensitive_action_can_queue_and_expired_lease_recovers():
    DatabaseCaseStore().ensure_schema()
    queue = AdminActionQueue()
    tenant = "test-" + uuid4().hex
    case_id = "case-" + uuid4().hex
    action = _action(requires_human_decision=False)
    try:
        item = queue.enqueue(
            tenant_id=tenant, case_id=case_id, action=action, requested_by="owner"
        )
        assert item["status"] == "queued"
        with SessionLocal() as db:
            row = db.query(AetherAdminActionRecord).filter_by(action_id=item["action_id"]).one()
            row.status = "running"
            row.locked_by = "dead-worker"
            row.lease_until = datetime.utcnow() - timedelta(seconds=1)
            row.attempts = 1
            db.commit()

        result = queue.dispatch(limit=1)
        assert result["dispatched"] == 1
        saved = queue.get(action_id=item["action_id"], tenant_id=tenant)
        assert saved["status"] == "dispatched"
        assert saved["attempts"] == 2
    finally:
        with SessionLocal() as db:
            db.query(AetherAdminActionRecord).filter_by(tenant_id=tenant).delete()
            db.commit()


def test_unsupported_external_action_is_rejected():
    queue = AdminActionQueue()
    with pytest.raises(ValueError, match="Unsupported"):
        queue.enqueue(
            tenant_id="tenant",
            case_id="case",
            action={"action_type": "submit_official_permit", "idempotency_key": "x"},
            requested_by="owner",
        )
