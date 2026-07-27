from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime


class AffordableHousing(Base):
    __tablename__ = "affordable_housings"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    applicant_name = Column(String)
    address = Column(String)
    district = Column(String)
    state = Column(String)
    annual_income = Column(Float, default=0.0)
    family_size = Column(Float, default=0)
    preferred_tenant_type = Column(String)  # ownership, rental
    monthly_rent_affordable = Column(Float, default=0.0)
    status = Column(String)  # applied, shortlisted, allotted, rejected
    allotted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
