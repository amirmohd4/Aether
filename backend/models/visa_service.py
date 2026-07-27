from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime


class VisaService(Base):
    __tablename__ = "visa_services"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    applicant_name = Column(String)
    passport_number = Column(String)
    visa_type = Column(String)  # tourist, business, student, work, transit
    destination_country = Column(String)
    duration_days = Column(Float, default=0)
    purpose = Column(String)
    entry_type = Column(String)  # single, multiple
    status = Column(String)  # applied, approved, rejected, issued
    visa_number = Column(String, nullable=True)
    fee_paid = Column(Boolean, default=False)
    amount_paid = Column(Float, default=0.0)
    issued_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
