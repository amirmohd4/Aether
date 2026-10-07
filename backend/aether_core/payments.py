from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Session

from .persistence_models import AetherPaymentRecord


class PaymentProvider:
    name = "abstract"

    def create_payment(self, payment_id: str, amount: int, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class DemoPaymentProvider(PaymentProvider):
    name = "demo"

    def create_payment(self, payment_id: str, amount: int, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "provider_payment_id": f"DEMO-{payment_id}",
            "status": "succeeded",
            "amount": amount,
            "currency": currency,
            "metadata": metadata,
        }


class PaymentService:
    """Idempotent payment ledger with replaceable provider implementation."""

    def __init__(self, session_factory, provider: PaymentProvider | None = None):
        self.session_factory = session_factory
        self.provider = provider or DemoPaymentProvider()

    def create(
        self,
        tenant_id: str,
        case_id: str,
        amount_minor: int,
        currency: str = "INR",
        idempotency_key: str | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        if amount_minor < 0:
            raise ValueError("Payment amount cannot be negative")
        key = idempotency_key or f"{case_id}:{amount_minor}:{currency}"
        with self.session_factory() as db:
            existing = db.query(AetherPaymentRecord).filter_by(
                tenant_id=tenant_id,
                idempotency_key=key,
            ).one_or_none()
            if existing:
                return self._serialize(existing)

            payment_id = f"PAY-{__import__('uuid').uuid4().hex[:16].upper()}"
            provider_result = self.provider.create_payment(
                payment_id,
                amount_minor,
                currency,
                metadata or {},
            )
            row = AetherPaymentRecord(
                payment_id=payment_id,
                tenant_id=tenant_id,
                case_id=case_id,
                amount_minor=amount_minor,
                currency=currency,
                provider=self.provider.name,
                provider_payment_id=provider_result.get("provider_payment_id"),
                status=provider_result.get("status", "pending"),
                idempotency_key=key,
                metadata_json=metadata or {},
                created_at=datetime.utcnow(),
                completed_at=datetime.utcnow() if provider_result.get("status") == "succeeded" else None,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return self._serialize(row)

    def for_case(self, tenant_id: str, case_id: str) -> list[Dict[str, Any]]:
        with self.session_factory() as db:
            rows = db.query(AetherPaymentRecord).filter_by(
                tenant_id=tenant_id,
                case_id=case_id,
            ).order_by(AetherPaymentRecord.id.desc()).all()
            return [self._serialize(row) for row in rows]

    @staticmethod
    def _serialize(row: AetherPaymentRecord) -> Dict[str, Any]:
        return {
            "payment_id": row.payment_id,
            "tenant_id": row.tenant_id,
            "case_id": row.case_id,
            "amount_minor": row.amount_minor,
            "currency": row.currency,
            "provider": row.provider,
            "provider_payment_id": row.provider_payment_id,
            "status": row.status,
            "idempotency_key": row.idempotency_key,
            "metadata": row.metadata_json or {},
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "completed_at": row.completed_at.isoformat() if row.completed_at else None,
        }
