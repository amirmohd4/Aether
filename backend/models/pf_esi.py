from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime


class PFESIRegistration(Base):
    __tablename__ = "pf_esi_registrations"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    employer_name = Column(String)
    establishment_name = Column(String)
    registration_type = Column(String)  # pf, esi
    employee_count = Column(Float, default=0)
    wage_ceiling = Column(Float, default=0.0)
    status = Column(String)  # applied, approved, rejected
    fee_paid = Column(Boolean, default=False)
    amount_paid = Column(Float, default=0.0)
    issued_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
