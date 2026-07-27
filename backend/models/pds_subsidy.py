from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime


class PDSSubsidy(Base):
    __tablename__ = "pds_subsidies"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    ration_card_id = Column(String)
    beneficiary_name = Column(String)
    subsidy_type = Column(String)  # food, lpg, fertilizer
    amount = Column(Float, default=0.0)
    bank_account = Column(String)
    ifsc_code = Column(String)
    status = Column(String)  # applied, approved, disbursed, rejected
    disbursed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
