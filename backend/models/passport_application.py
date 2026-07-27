from sqlalchemy import Column, String, DateTime, Boolean, JSON
from database import Base
from datetime import datetime


class PassportApplication(Base):
    __tablename__ = "passport_applications"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    applicant_name = Column(String)
    passport_type = Column(String)  # fresh, renewal, tatkal
    date_of_birth = Column(DateTime)
    place_of_birth = Column(String)
    address = Column(String)
    district = Column(String)
    state = Column(String)
    aadhaar_number = Column(String)
    purpose = Column(String)  # travel, employment, education
    travel_country = Column(String, nullable=True)
    status = Column(String)  # applied, police_verification, issued, rejected
    passport_number = Column(String, nullable=True)
    fee_paid = Column(Boolean, default=False)
    issued_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
