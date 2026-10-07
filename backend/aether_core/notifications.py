from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from .persistence_models import AetherNotificationRecord


class NotificationService:
    """Transactional-style outbox for Aether case notifications."""

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
    ) -> Dict[str, Any]:
        from .case_store import DatabaseCaseStore
        DatabaseCaseStore().ensure_schema()
        if channel not in self.CHANNELS:
            raise ValueError(f"Unsupported notification channel: {channel}")
        with self.session_factory() as db:
            row = AetherNotificationRecord(
                tenant_id=tenant_id,
                user_id=user_id,
                case_id=case_id,
                event_type=event_type,
                channel=channel,
                destination=destination,
                status="queued",
                payload=payload or {},
                created_at=datetime.utcnow(),
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return self._serialize(row)

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
            rows = query.order_by(AetherNotificationRecord.id.desc()).limit(max(1, min(limit, 100))).all()
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
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "sent_at": row.sent_at.isoformat() if row.sent_at else None,
        }
