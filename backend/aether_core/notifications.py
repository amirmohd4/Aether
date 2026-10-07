from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import Session

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


    def dispatch_queued(self, limit: int = 50) -> Dict[str, Any]:
        """Deliver in-app messages and configured webhooks; leave unsupported channels queued."""
        import os
        import httpx
        with self.session_factory() as db:
            rows = db.query(AetherNotificationRecord).filter(
                AetherNotificationRecord.status == "queued"
            ).order_by(AetherNotificationRecord.id.asc()).limit(max(1, min(limit, 100))).all()
            delivered = 0
            failed = 0
            webhook = os.getenv("AETHER_NOTIFICATION_WEBHOOK_URL", "").strip()
            for row in rows:
                try:
                    if row.channel == "in_app":
                        row.status = "sent"
                    elif row.channel == "webhook" and webhook:
                        response = httpx.post(
                            webhook,
                            json={
                                "event_type": row.event_type,
                                "case_id": row.case_id,
                                "tenant_id": row.tenant_id,
                                "payload": row.payload or {},
                            },
                            timeout=10.0,
                        )
                        response.raise_for_status()
                        row.status = "sent"
                    else:
                        continue
                    row.sent_at = datetime.utcnow()
                    delivered += 1
                except Exception:
                    row.status = "failed"
                    failed += 1
            db.commit()
            return {"delivered": delivered, "failed": failed, "remaining": len(rows) - delivered - failed}

    def list_for_tenant(
        self,
        tenant_id: str,
        case_id: str | None = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
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
