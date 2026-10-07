from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.types import JSON

from backend.database import Base, engine


# The private execution-core schema is a PostgreSQL concern. SQLite is used by
# local development and CI, where SQLAlchemy schemas are not supported.
PERSISTENCE_SCHEMA = "aether_internal" if engine.dialect.name == "postgresql" else None


class AetherCaseRecord(Base):
    __tablename__ = "aether_v2_cases"
    __table_args__ = {"schema": PERSISTENCE_SCHEMA}

    case_id = Column(String(64), primary_key=True)
    status = Column(String(64), nullable=False, index=True)
    objective = Column(Text, nullable=False)
    customer_type = Column(String(64), nullable=False, index=True)
    owner_user_id = Column(String(128), nullable=True, index=True)
    tenant_id = Column(String(128), nullable=True, index=True)
    service_id = Column(String(128), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    payload = Column(JSON, nullable=False)


class AetherExecutionEventRecord(Base):
    __tablename__ = "aether_v2_execution_events"
    __table_args__ = {"schema": PERSISTENCE_SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String(64), nullable=False, index=True)
    action = Column(String(128), nullable=False, index=True)
    actor = Column(String(128), nullable=False)
    tenant_id = Column(String(128), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    data = Column(JSON, nullable=False)
    previous_hash = Column(String(128), nullable=True)
    event_hash = Column(String(128), nullable=False, index=True)


class AetherTaskQueueRecord(Base):
    __tablename__ = "aether_v2_task_queue"
    __table_args__ = (
        UniqueConstraint("case_id", "task_id", name="uq_aether_task_queue_case_task"),
        {"schema": PERSISTENCE_SCHEMA},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String(64), nullable=False, index=True)
    task_id = Column(String(128), nullable=False)
    status = Column(String(32), nullable=False, index=True)
    available_at = Column(DateTime(timezone=True), nullable=False, index=True)
    locked_by = Column(String(128), nullable=True, index=True)
    lease_until = Column(DateTime(timezone=True), nullable=True, index=True)
    attempts = Column(Integer, nullable=False, default=0)
    last_error = Column(Text, nullable=True)
    payload = Column(JSON, nullable=False, default=dict)


class AetherTaskCheckpointRecord(Base):
    __tablename__ = "aether_v2_task_checkpoints"
    __table_args__ = {"schema": PERSISTENCE_SCHEMA}

    case_id = Column(String(64), primary_key=True)
    task_id = Column(String(128), primary_key=True)
    status = Column(String(32), nullable=False, index=True)
    result = Column(JSON, nullable=True)
    evidence = Column(JSON, nullable=False, default=list)
    error = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    attempts = Column(Integer, nullable=False, default=0)
    idempotency_key = Column(String(256), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=False)


class AetherDocumentRecord(Base):
    __tablename__ = "aether_v2_documents"
    __table_args__ = {"schema": PERSISTENCE_SCHEMA}

    document_id = Column(String(64), primary_key=True)
    case_id = Column(String(64), nullable=False, index=True)
    tenant_id = Column(String(128), nullable=True, index=True)
    owner_user_id = Column(String(128), nullable=True, index=True)
    document_type = Column(String(128), nullable=False, index=True)
    filename = Column(String(512), nullable=False)
    mime_type = Column(String(128), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    sha256 = Column(String(128), nullable=False, index=True)
    storage_key = Column(Text, nullable=False)
    extracted_text = Column(Text, nullable=False, default="")
    extraction_mode = Column(String(64), nullable=False, default="metadata-only")
    created_at = Column(DateTime(timezone=True), nullable=False)


class AetherNotificationRecord(Base):
    __tablename__ = "aether_v2_notifications"
    __table_args__ = {"schema": PERSISTENCE_SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(128), nullable=True, index=True)
    user_id = Column(String(128), nullable=True, index=True)
    case_id = Column(String(64), nullable=True, index=True)
    event_type = Column(String(128), nullable=False, index=True)
    channel = Column(String(32), nullable=False)
    destination = Column(String(512), nullable=True)
    status = Column(String(32), nullable=False, index=True)
    payload = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)


class AetherPaymentRecord(Base):
    __tablename__ = "aether_v2_payments"
    __table_args__ = (
        UniqueConstraint("tenant_id", "idempotency_key", name="uq_aether_payment_tenant_key"),
        {"schema": PERSISTENCE_SCHEMA},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(String(64), unique=True, nullable=False, index=True)
    tenant_id = Column(String(128), nullable=False, index=True)
    case_id = Column(String(64), nullable=False, index=True)
    amount_minor = Column(Integer, nullable=False)
    currency = Column(String(8), nullable=False, default="INR")
    provider = Column(String(64), nullable=False)
    provider_payment_id = Column(String(128), nullable=True)
    status = Column(String(32), nullable=False, index=True)
    idempotency_key = Column(String(256), nullable=False)
    metadata_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class AetherUsageRecord(Base):
    __tablename__ = "aether_v2_usage"
    __table_args__ = (
        UniqueConstraint("tenant_id", "case_id", "event_type", name="uq_aether_usage_case_event"),
        {"schema": PERSISTENCE_SCHEMA},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(128), nullable=False, index=True)
    case_id = Column(String(64), nullable=True, index=True)
    customer_type = Column(String(64), nullable=True, index=True)
    event_type = Column(String(64), nullable=False, index=True)
    units = Column(Integer, nullable=False, default=1)
    unit_type = Column(String(32), nullable=False, default="case")
    created_at = Column(DateTime(timezone=True), nullable=False)
    metadata_json = Column(JSON, nullable=False, default=dict)


def utc_datetime() -> datetime:
    return datetime.utcnow()
