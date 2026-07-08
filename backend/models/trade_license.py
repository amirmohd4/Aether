from sqlalchemy import Column, String, Float, DateTime, Boolean, JSON
from database import Base
from datetime import datetime

class TradeLicense(Base):
    __tablename__ = "trade_licenses"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    business_name = Column(String)
    business_type = Column(String)
    address = Column(String)
    status = Column(String)  # applied, under_review, approved, rejected
    nocs = Column(JSON, default={})  # { "fire": "pending", "health": "approved" }
    fee_paid = Column(Boolean, default=False)
    amount_paid = Column(Float, default=0.0)
    issued_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
