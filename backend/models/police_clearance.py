from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime


class PoliceClearanceCertificate(Base):
    __tablename__ = "police_clearance_certificates"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    applicant_name = Column(String)
    father_name = Column(String)
    address = Column(String)
    district = Column(String)
    state = Column(String)
    purpose = Column(String)  # employment, immigration, visa, other
    passport_number = Column(String, nullable=True)
    status = Column(String)  # applied, under_verification, issued, rejected
    fee_paid = Column(Boolean, default=False)
    issued_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
