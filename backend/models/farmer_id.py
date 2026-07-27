from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime


class FarmerID(Base):
    __tablename__ = "farmer_ids"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    farmer_name = Column(String)
    father_name = Column(String)
    village = Column(String)
    tehsil = Column(String)
    district = Column(String)
    state = Column(String)
    land_area_acres = Column(Float, default=0.0)
    survey_number = Column(String)
    crop_type = Column(String)
    status = Column(String)  # applied, approved, rejected
    issued_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
