from sqlalchemy import Column, String, DateTime, Boolean, Float
from database import Base
from datetime import datetime

class MedicalLicense(Base):
    __tablename__ = "medical_licenses"

    id = Column(String, primary_key=True)
    doctor_name = Column(String)
    doctor_id = Column(String, index=True)
    qualification = Column(String)
    institution = Column(String)
    status = Column(String)  # applied, under_review, approved, rejected
    fee_paid = Column(Boolean, default=False)
    amount_paid = Column(Float, default=0.0)
    issued_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
