from sqlalchemy import Column, String, Float, DateTime, Boolean, JSON
from database import Base
from datetime import datetime


class RationCard(Base):
    __tablename__ = "ration_cards"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    head_of_family = Column(String)
    card_type = Column(String)  # AAY, BPL, APL
    address = Column(String)
    district = Column(String)
    state = Column(String)
    members = Column(JSON, default=[])  # list of member names
    annual_income = Column(Float, default=0.0)
    status = Column(String)  # applied, approved, rejected
    issued_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
