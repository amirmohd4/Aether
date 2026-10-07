from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.types import JSON

from backend.database import Base


class AetherCaseRecord(Base):
    __tablename__ = "aether_v2_cases"

    case_id = Column(String(64), primary_key=True)
    status = Column(String(64), nullable=False, index=True)
    objective = Column(Text, nullable=False)
    customer_type = Column(String(64), nullable=False, index=True)
    service_id = Column(String(128), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    payload = Column(JSON, nullable=False)


class AetherExecutionEventRecord(Base):
    __tablename__ = "aether_v2_execution_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String(64), nullable=False, index=True)
    action = Column(String(128), nullable=False, index=True)
    actor = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    data = Column(JSON, nullable=False)


def utc_datetime() -> datetime:
    return datetime.utcnow()
