from __future__ import annotations

from datetime import datetime
import os

from sqlalchemy import Column, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.types import JSON

from backend.database import Base


PERSISTENCE_SCHEMA = "aether_internal" if os.getenv("DATABASE_URL") else None


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


def utc_datetime() -> datetime:
    return datetime.utcnow()


class AetherUsageRecord(Base):
    __tablename__ = "aether_v2_usage"
    __table_args__ = {"schema": PERSISTENCE_SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(128), nullable=False, index=True)
    case_id = Column(String(64), nullable=True, index=True)
    customer_type = Column(String(64), nullable=True, index=True)
    event_type = Column(String(64), nullable=False, index=True)
    units = Column(Integer, nullable=False, default=1)
    unit_type = Column(String(32), nullable=False, default="case")
    created_at = Column(DateTime(timezone=True), nullable=False)
    metadata_json = Column(JSON, nullable=False, default=dict)
