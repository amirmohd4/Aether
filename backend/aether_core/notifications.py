from __future__ import annotations

from datetime import datetime, timedelta
import hashlib
import hmac
import json
import os
import socket
from typing import Any, Dict, List
from uuid import uuid4

import httpx

from .persistence_models import AetherNotificationRecord


class NotificationService:
    """Durable notification outbox with idempotency, leases and bounded retries."""

    CHANNELS = {"in_app", "email", "sms", "webhook"}

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def enqueue(
        self,
        tenant_id: str | None,
        user_id: str | None,
        case_id: str | None,
        event_type: str,
        channel: str = "in_app",
        destination: str | None = None,
        payload: Dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Dict[str, Any]:
        if channel not in self.CHANNELS:
            raise ValueError(f"Unsupported notification channel: {channel}")

        key = idempotency_key or (
            f"{tenant_id or 'unscoped'}:{case_id or 'workspace'}:"
            f"{event_type}:{channel}:{destination or 'default'}"
        )
        from .case_store import DatabaseCaseStore
        DatabaseCaseStore().ensure_schema()

        with self.session_factory() as db:
            existing = db.query(AetherNotificationRecord).filter_by(
                tenant_id=tenant_id,
                idempotency_key=key,
            ).one_or_none()
            if existing:
                return self._serialize(existing)

            row = AetherNotificationRecord(
                tenant_id=tenant_id,
                user_id=user_id,
                case_id=case_id,
                event_type=event_type,
                channel=channel,
                destination=destination,
                status="queued",
                payload=payload or {},
                idempotency_key=key,
                attempts=0,
                created_at=datetime.utcnow(),
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return self._serialize(row)

    def dispatch_queued(self, limit: int = 50) -> Dict[str, Any]:
        """Deliver queued notifications without double-send races."""
        max_attempts = max(1, int(os.getenv("AETHER_NOTIFICATION_MAX_ATTEMPTS", "3")))
        worker_id = f"{socket.gethostname()}:{os.getpid()}:{uuid4().hex[:8]}"
        delivered = 0
        failed = 0

        for _ in range(max(1, min(limit, 100))):
            item = self._claim_one(worker_id)
            if item is None:
                break
            try:
                self._deliver(item)
                self._finalize(item["id"], worker_id, "sent", None)
                delivered += 1
            except Exception as exc:
                next_status = "failed" if item["attempts"] >= max_attempts else "queued"
                self._finalize(item["id"], worker_id, next_status, str(exc))
                if next_status == "failed":
                    failed += 1

        with self.session_factory() as db:
            remaining = db.query(AetherNotificationRecord).filter(
                AetherNotificationRecord.status.in_(["queued", "sending"])
            ).count()
        return {"delivered": delivered, "failed": failed, "remaining": remaining}

    def _claim_one(self, worker_id: str) -> Dict[str, Any] | None:
        now = datetime.utcnow()
        lease_until = now + timedelta(seconds=60)
        with self.session_factory() as db:
            row = (
                db.query(AetherNotificationRecord)
                .filter(
                    (AetherNotificationRecord.status == "queued")
                    | (
                        (AetherNotificationRecord.status == "sending")
                        & AetherNotificationRecord.lease_until.isnot(None)
                        & (AetherNotificationRecord.lease_until < now)
                    )
                )
                .order_by(AetherNotificationRecord.id.asc())
                .with_for_update(skip_locked=True)
                .first()
            )
            if row is None:
                return None
            row.status = "sending"
            row.locked_by = worker_id
            row.lease_until = lease_until
            row.attempts = (row.attempts or 0) + 1
            db.commit()
            return self._serialize(row)

    def _deliver(self, item: Dict[str, Any]) -> None:
        if item["channel"] == "in_app":
            return

        channel = item["channel"]
        if channel == "webhook":
            url = os.getenv("AETHER_NOTIFICATION_WEBHOOK_URL", "").strip()
        elif channel == "email":
            url = os.getenv("AETHER_NOTIFICATION_EMAIL_URL", "").strip()
        elif channel == "sms":
            url = os.getenv("AETHER_NOTIFICATION_SMS_URL", "").strip()
        else:
            url = ""

        if not url:
            raise RuntimeError(f"No notification provider configured for {channel}")

        body = {
            "event_type": item["event_type"],
            "case_id": item["case_id"],
            "tenant_id": item["tenant_id"],
            "user_id": item["user_id"],
            "payload": item["payload"],
        }
        raw = json.dumps(body, separators=(",", ":"), sort_keys=True).encode("utf-8")
        secret = os.getenv("AETHER_NOTIFICATION_WEBHOOK_SECRET", "").strip()
        headers = {"Content-Type": "application/json"}
        if secret:
            headers["X-Aether-Signature"] = hmac.new(
                secret.encode("utf-8"),
                raw,
                hashlib.sha256,
            ).hexdigest()

        response = httpx.post(url, content=raw, headers=headers, timeout=15.0)
        response.raise_for_status()

    def _finalize(
        self,
        row_id: int,
        worker_id: str,
        status: str,
        error: str | None,
    ) -> None:
        with self.session_factory() as db:
            row = db.get(AetherNotificationRecord, row_id)
            if row is None or row.locked_by != worker_id:
                return
            row.status = status
            row.last_error = error
            row.locked_by = None
            row.lease_until = None
            if status == "sent":
                row.sent_at = datetime.utcnow()
            db.commit()

    def list_for_tenant(
        self,
        tenant_id: str,
        case_id: str | None = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        from .case_store import DatabaseCaseStore
        DatabaseCaseStore().ensure_schema()
        with self.session_factory() as db:
            query = db.query(AetherNotificationRecord).filter(
                AetherNotificationRecord.tenant_id == tenant_id
            )
            if case_id:
                query = query.filter(AetherNotificationRecord.case_id == case_id)
            rows = (
                query.order_by(AetherNotificationRecord.id.desc())
                .limit(max(1, min(limit, 100)))
                .all()
            )
            return [self._serialize(row) for row in rows]

    @staticmethod
    def _serialize(row: AetherNotificationRecord) -> Dict[str, Any]:
        return {
            "id": row.id,
            "tenant_id": row.tenant_id,
            "user_id": row.user_id,
            "case_id": row.case_id,
            "event_type": row.event_type,
            "channel": row.channel,
            "destination": row.destination,
            "status": row.status,
            "payload": row.payload or {},
            "idempotency_key": row.idempotency_key,
            "attempts": row.attempts,
            "last_error": row.last_error,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "sent_at": row.sent_at.isoformat() if row.sent_at else None,
        }
