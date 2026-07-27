from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime


class GSTRegistration(Base):
    __tablename__ = "gst_registrations"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    business_name = Column(String)
    business_type = Column(String)  # proprietorship, partnership, pvt_ltd, public_ltd
    pan_number = Column(String)
    aadhaar_number = Column(String)
    address = Column(String)
    district = Column(String)
    state = Column(String)
    turnover = Column(Float, default=0.0)
    status = Column(String)  # applied, approved, rejected
    gstin = Column(String, nullable=True)
    fee_paid = Column(Boolean, default=False)
    issued_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
