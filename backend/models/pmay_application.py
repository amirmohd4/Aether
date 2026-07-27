from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime


class PMAYApplication(Base):
    __tablename__ = "pmay_applications"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    applicant_name = Column(String)
    spouse_name = Column(String, nullable=True)
    address = Column(String)
    district = Column(String)
    state = Column(String)
    annual_income = Column(Float, default=0.0)
    category = Column(String)  # EWS, LIG, MIG_I, MIG_II
    carpet_area_required = Column(Float, default=0.0)
    aadhaar_number = Column(String)
    status = Column(String)  # applied, approved, rejected, sanctioned
    subsidy_amount = Column(Float, default=0.0)
    sanctioned_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
