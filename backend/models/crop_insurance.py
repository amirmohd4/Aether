from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime


class CropInsurance(Base):
    __tablename__ = "crop_insurances"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    farmer_id = Column(String)
    farmer_name = Column(String)
    crop_name = Column(String)
    area_acres = Column(Float, default=0.0)
    sum_insured = Column(Float, default=0.0)
    premium_amount = Column(Float, default=0.0)
    season = Column(String)  # kharif, rabi
    village = Column(String)
    district = Column(String)
    state = Column(String)
    status = Column(String)  # applied, approved, claim_settled, rejected
    claim_amount = Column(Float, default=0.0)
    claim_settled_at = Column(DateTime, nullable=True)
    issued_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
