"""Durable, idempotent queue for internal administrative work items.

The worker only dispatches internal follow-up work. It never files forms, changes
legal status, approves permits, certifies work, or releases money.
"""
from __future__ import annotations

from datetime import datetime, timedelta
import hashlib
import os
import socket
from typing import Any
from uuid import uuid4

from sqlalchemy import or_

from backend.database import SessionLocal
from .case_store import DatabaseCaseStore
from .persistence_models import AetherAdminActionRecord


LEASE_SECONDS = 60
MAX_ATTEMPTS = 5
SAFE_INTERNAL_ACTIONS = {
    "collect_approved_budget",
    "request_cost_to_complete_forecast",
    "prepare_cost_variance_and_change_order_review",
    "escalate_commitment_register",
    "prepare_schedule_recovery_plan",
    "verify_permit_status_and_source_evidence",
    "request_permit_receipt_or_certificate",
    "assign_accountable_milestone_owner",
    "request_completion_evidence_or_recovery_action",
    "assign_dependency_owner_and_next_action",
    "assemble_missing_payment_claim_evidence",
    "resolve_cross_department_handoff",
}


def _now() -> datetime:
    return datetime.utcnow()


def _serialize(row: AetherAdminActionRecord) -> dict[str, Any]:
    return {
        "action_id": row.action_id,
        "case_id": row.case_id,
        "tenant_id": row.tenant_id,
        "action_type": row.action_type,
        "status": row.status,
        "priority": row.priority,
        "payload": row.payload or {},
        "outcome": row.outcome,
        "attempts": row.attempts,
        "requested_by": row.requested_by,
        "approved_by": row.approved_by,
        "approved_at": row.approved_at.isoformat() if row.approved_at else None,
        "last_error": row.last_error,
        "created_at": row.created_at.isoformat(),
        "updated_at": row.updated_at.isoformat(),
        "verified_at": row.verified_at.isoformat() if row.verified_at else None,
    }


class AdminActionQueue:
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def enqueue(
        self,
        *,
        tenant_id: str,
        case_id: str,
        action: dict[str, Any],
        requested_by: str,
        approved_by: str | None = None,
    ) -> dict[str, Any]:
        if not tenant_id:
            raise ValueError("A tenant is required for administrative actions")
        action_type = str(action.get("action_type") or "")
        if action_type not in SAFE_INTERNAL_ACTIONS:
            raise ValueError("Unsupported administrative action type")
        key = str(action.get("idempotency_key") or "")
        if not key:
            raise ValueError("An idempotency key is required")
        if action.get("requires_human_decision") and not approved_by:
            initial_status = "awaiting_approval"
        else:
            initial_status = "queued"
        action_id = "adm_" + hashlib.sha256(
            f"{tenant_id}:{case_id}:{key}".encode("utf-8")
        ).hexdigest()[:24]
        DatabaseCaseStore().ensure_schema()
        now = _now()
        with self.session_factory() as db:
            existing = db.query(AetherAdminActionRecord).filter_by(
                tenant_id=tenant_id, idempotency_key=key
            ).one_or_none()
            if existing:
                return _serialize(existing)
            row = AetherAdminActionRecord(
                action_id=action_id,
                tenant_id=tenant_id,
                case_id=case_id,
                action_type=action_type,
                status=initial_status,
                priority=str(action.get("priority") or "normal"),
                idempotency_key=key,
                payload={**action, "execution_mode": "internal_work_item_only"},
                outcome=None,
                attempts=0,
                available_at=now,
                requested_by=requested_by,
                approved_by=approved_by,
                approved_at=now if approved_by else None,
                created_at=now,
                updated_at=now,
            )
            db.add(row)
            try:
                db.commit()
                db.refresh(row)
                return _serialize(row)
            except Exception:
                db.rollback()
                existing = db.query(AetherAdminActionRecord).filter_by(
                    tenant_id=tenant_id, idempotency_key=key
                ).one_or_none()
                if existing:
                    return _serialize(existing)
                raise

    def approve(self, *, action_id: str, tenant_id: str, approver: str) -> dict[str, Any]:
        DatabaseCaseStore().ensure_schema()
        with self.session_factory() as db:
            row = db.query(AetherAdminActionRecord).filter_by(
                action_id=action_id, tenant_id=tenant_id
            ).with_for_update().one_or_none()
            if row is None:
                raise KeyError(action_id)
            if row.requested_by == approver:
                raise ValueError("A different authorized reviewer must approve this action")
            if row.status == "queued" and row.approved_by:
                return _serialize(row)
            if row.status != "awaiting_approval":
                raise ValueError(f"Action cannot be approved from status {row.status}")
            row.approved_by = approver
            row.approved_at = _now()
            row.status = "queued"
            row.updated_at = _now()
            db.commit()
            db.refresh(row)
            return _serialize(row)

    def get(self, *, action_id: str, tenant_id: str) -> dict[str, Any]:
        DatabaseCaseStore().ensure_schema()
        with self.session_factory() as db:
            row = db.query(AetherAdminActionRecord).filter_by(
                action_id=action_id, tenant_id=tenant_id
            ).one_or_none()
            if row is None:
                raise KeyError(action_id)
            return _serialize(row)

    def list_for_case(self, *, case_id: str, tenant_id: str) -> list[dict[str, Any]]:
        DatabaseCaseStore().ensure_schema()
        with self.session_factory() as db:
            rows = db.query(AetherAdminActionRecord).filter_by(
                case_id=case_id, tenant_id=tenant_id
            ).order_by(AetherAdminActionRecord.created_at.desc()).limit(100).all()
            return [_serialize(row) for row in rows]

    def _claim_one(self, worker_id: str) -> dict[str, Any] | None:
        now = _now()
        DatabaseCaseStore().ensure_schema()
        with self.session_factory() as db:
            row = (
                db.query(AetherAdminActionRecord)
                .filter(
                    or_(
                        (AetherAdminActionRecord.status == "queued")
                        & (AetherAdminActionRecord.available_at <= now),
                        (AetherAdminActionRecord.status == "running")
                        & AetherAdminActionRecord.lease_until.isnot(None)
                        & (AetherAdminActionRecord.lease_until < now),
                    )
                )
                .order_by(AetherAdminActionRecord.created_at.asc())
                .with_for_update(skip_locked=True)
                .first()
            )
            if row is None:
                return None
            if row.attempts >= MAX_ATTEMPTS:
                row.status = "failed"
                row.last_error = row.last_error or "Maximum attempts exceeded"
                row.locked_by = None
                row.lease_until = None
                row.updated_at = now
                db.commit()
                return {"terminal": True}
            row.status = "running"
            row.locked_by = worker_id
            row.lease_until = now + timedelta(seconds=LEASE_SECONDS)
            row.attempts += 1
            row.updated_at = now
            payload = {
                "action_id": row.action_id,
                "tenant_id": row.tenant_id,
                "case_id": row.case_id,
                "action_type": row.action_type,
                "payload": row.payload or {},
                "attempts": row.attempts,
            }
            db.commit()
            return payload

    def _finalize(self, item: dict[str, Any], worker_id: str, success: bool, error: str | None = None) -> None:
        now = _now()
        with self.session_factory() as db:
            row = db.query(AetherAdminActionRecord).filter_by(
                action_id=item["action_id"], locked_by=worker_id, status="running"
            ).with_for_update().one_or_none()
            if row is None:
                return
            row.locked_by = None
            row.lease_until = None
            row.updated_at = now
            if success:
                # "dispatched" means the internal follow-up was materialized and
                # verified, not that a department or authority completed it.
                row.status = "dispatched"
                row.outcome = {
                    "kind": "internal_work_item_dispatched",
                    "verified": True,
                    "verified_checks": [
                        "tenant_and_case_bound",
                        "action_type_allowlisted",
                        "durable_queue_record_reloaded",
                    ],
                    "external_effect": False,
                    "next_step": "Assigned staff must complete the work and attach source-backed evidence.",
                }
                row.verified_at = now
                row.last_error = None
            else:
                row.last_error = (error or "Unknown worker error")[:2000]
                if row.attempts >= MAX_ATTEMPTS:
                    row.status = "failed"
                else:
                    row.status = "queued"
                    row.available_at = now + timedelta(seconds=min(300, 2 ** row.attempts * 5))
            db.commit()

    def dispatch(self, limit: int = 20) -> dict[str, Any]:
        worker_id = f"{socket.gethostname()}:{os.getpid()}:{uuid4().hex[:8]}"
        dispatched = 0
        failed = 0
        inspected = 0
        for _ in range(max(1, min(int(limit), 100))):
            item = self._claim_one(worker_id)
            if item is None:
                break
            inspected += 1
            if item.get("terminal"):
                failed += 1
                continue
            try:
                # The worker only validates and dispatches an internal follow-up
                # work item. It intentionally has no connector capable of filing,
                # approving, certifying, paying, or mutating an external system.
                if item["action_type"] not in SAFE_INTERNAL_ACTIONS:
                    raise ValueError("Action type is not on the internal allowlist")
                current = self.get(action_id=item["action_id"], tenant_id=item["tenant_id"])
                if current["status"] != "running" or current["case_id"] != item["case_id"]:
                    raise RuntimeError("Queue ownership or state verification failed")
                self._finalize(item, worker_id, True)
                dispatched += 1
            except Exception as exc:
                self._finalize(item, worker_id, False, str(exc))
                failed += 1
        return {"inspected": inspected, "dispatched": dispatched, "failed_or_exhausted": failed}
