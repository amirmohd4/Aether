from sqlalchemy import Column, String, Float, DateTime, Boolean, JSON
from database import Base
from datetime import datetime


class RERAProject(Base):
    __tablename__ = "rera_projects"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    developer_name = Column(String)
    project_name = Column(String)
    project_type = Column(String)  # residential, commercial, mixed
    project_address = Column(String)
    district = Column(String)
    state = Column(String)
    land_area = Column(Float, default=0.0)
    total_units = Column(Float, default=0)
    estimated_cost = Column(Float, default=0.0)
    completion_date = Column(DateTime, nullable=True)
    status = Column(String)  # applied, approved, rejected
    rera_number = Column(String, nullable=True)
    fee_paid = Column(Boolean, default=False)
    amount_paid = Column(Float, default=0.0)
    issued_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
