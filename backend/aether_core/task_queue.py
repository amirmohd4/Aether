from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import os
import socket
from threading import Lock
from typing import Any, Dict, List, Optional
from uuid import uuid4

from sqlalchemy import and_
from .case_store import DatabaseCaseStore
from .persistence_models import AetherTaskQueueRecord
from backend.database import SessionLocal


@dataclass(frozen=True)
class TaskClaim:
    queue_id: int
    case_id: str
    task_id: str
    worker_id: str
    attempts: int
    payload: Dict[str, Any]


class DurableTaskQueue:
    """PostgreSQL/SQLite-backed queue with leases and recovery.

    The queue is intentionally independent of the execution worker. A task is
    first persisted, then atomically claimed for a short lease. Expired leases
    can be reclaimed after a process crash.
    """

    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

    def __init__(self, lease_seconds: int = 120, worker_id: Optional[str] = None) -> None:
        self.lease_seconds = lease_seconds
        self.worker_id = worker_id or f"{socket.gethostname()}:{os.getpid()}:{uuid4().hex[:8]}"
        self._schema_lock = Lock()
        self._schema_ready = False
        self._store = DatabaseCaseStore()

    def _ensure_schema(self) -> None:
        self._store._ensure_schema()
        self._schema_ready = True

    def enqueue(
        self,
        case_id: str,
        task_id: str,
        payload: Dict[str, Any] | None = None,
        available_at: datetime | None = None,
    ) -> AetherTaskQueueRecord:
        self._ensure_schema()
        now = datetime.utcnow()
        with SessionLocal() as db:
            row = db.query(AetherTaskQueueRecord).filter_by(
                case_id=case_id, task_id=task_id
            ).one_or_none()
            if row is None:
                row = AetherTaskQueueRecord(
                    case_id=case_id,
                    task_id=task_id,
                    status=self.READY,
                    available_at=available_at or now,
                    payload=payload or {},
                    attempts=0,
                )
                db.add(row)
            elif row.status in {self.FAILED, self.COMPLETED}:
                row.status = self.READY
                row.available_at = available_at or now
                row.locked_by = None
                row.lease_until = None
                row.last_error = None
                row.payload = payload or row.payload or {}
            db.commit()
            db.refresh(row)
            return row

    def claim(self, case_id: str | None = None) -> TaskClaim | None:
        self._ensure_schema()
        now = datetime.utcnow()
        with SessionLocal() as db:
            base = db.query(AetherTaskQueueRecord).filter(
                AetherTaskQueueRecord.status == self.READY,
                AetherTaskQueueRecord.available_at <= now,
            )
            if case_id:
                base = base.filter(AetherTaskQueueRecord.case_id == case_id)

            # A live lease is not claimable. Stale RUNNING rows are reclaimed below.
            row = base.order_by(AetherTaskQueueRecord.id.asc()).with_for_update(
                skip_locked=True
            ).first()
            if row is None:
                return None

            row.status = self.RUNNING
            row.locked_by = self.worker_id
            row.lease_until = now + timedelta(seconds=self.lease_seconds)
            row.attempts += 1
            db.commit()
            db.refresh(row)
            return TaskClaim(
                queue_id=row.id,
                case_id=row.case_id,
                task_id=row.task_id,
                worker_id=self.worker_id,
                attempts=row.attempts,
                payload=row.payload or {},
            )

    def complete(self, queue_id: int) -> None:
        self._ensure_schema()
        with SessionLocal() as db:
            row = db.get(AetherTaskQueueRecord, queue_id)
            if row is None:
                raise KeyError(queue_id)
            row.status = self.COMPLETED
            row.locked_by = None
            row.lease_until = None
            row.last_error = None
            db.commit()

    def fail(
        self,
        queue_id: int,
        error: str,
        retry: bool = True,
        retry_delay_seconds: int = 5,
    ) -> None:
        self._ensure_schema()
        now = datetime.utcnow()
        with SessionLocal() as db:
            row = db.get(AetherTaskQueueRecord, queue_id)
            if row is None:
                raise KeyError(queue_id)
            if retry:
                row.status = self.READY
                row.available_at = now + timedelta(seconds=retry_delay_seconds)
            else:
                row.status = self.FAILED
            row.locked_by = None
            row.lease_until = None
            row.last_error = error
            db.commit()

    def reclaim_expired(self, case_id: str | None = None) -> int:
        self._ensure_schema()
        now = datetime.utcnow()
        with SessionLocal() as db:
            query = db.query(AetherTaskQueueRecord).filter(
                AetherTaskQueueRecord.status == self.RUNNING,
                AetherTaskQueueRecord.lease_until.isnot(None),
                AetherTaskQueueRecord.lease_until < now,
            )
            if case_id:
                query = query.filter(AetherTaskQueueRecord.case_id == case_id)
            rows = query.all()
            for row in rows:
                row.status = self.READY
                row.available_at = now
                row.locked_by = None
                row.lease_until = None
                row.last_error = row.last_error or "Lease expired; task returned to queue."
            db.commit()
            return len(rows)

    def for_case(self, case_id: str) -> List[Dict[str, Any]]:
        self._ensure_schema()
        with SessionLocal() as db:
            rows = db.query(AetherTaskQueueRecord).filter(
                AetherTaskQueueRecord.case_id == case_id
            ).order_by(AetherTaskQueueRecord.id.asc()).all()
            return [
                {
                    "id": row.id,
                    "case_id": row.case_id,
                    "task_id": row.task_id,
                    "status": row.status,
                    "available_at": row.available_at.isoformat() if row.available_at else None,
                    "locked_by": row.locked_by,
                    "lease_until": row.lease_until.isoformat() if row.lease_until else None,
                    "attempts": row.attempts,
                    "last_error": row.last_error,
                }
                for row in rows
            ]
