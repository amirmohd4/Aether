from sqlalchemy import Column, String, Float, DateTime, Boolean, JSON
from database import Base
from datetime import datetime

class BuildingPermit(Base):
    __tablename__ = "building_permits"

    id = Column(String, primary_key=True)
    property_id = Column(String, index=True)
    developer_id = Column(String, index=True)
    project_name = Column(String)
    project_type = Column(String)  # residential, commercial, industrial
    plan_url = Column(String)
    status = Column(String)  # applied, scrutiny, nocs, approved, rejected
    nocs = Column(JSON, default={})
    scrutiny_score = Column(Float, default=0.0)
    scrutiny_issues = Column(JSON, default=[])
    fee_paid = Column(Boolean, default=False)
    amount_paid = Column(Float, default=0.0)
    issued_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
