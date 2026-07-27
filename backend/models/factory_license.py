from sqlalchemy import Column, String, Float, DateTime, Boolean, JSON
from database import Base
from datetime import datetime


class FactoryLicense(Base):
    __tablename__ = "factory_licenses"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    factory_name = Column(String)
    factory_type = Column(String)
    address = Column(String)
    district = Column(String)
    state = Column(String)
    employee_count = Column(Float, default=0)
    machinery_details = Column(String)
    status = Column(String)
    nocs = Column(JSON, default={})
    fee_paid = Column(Boolean, default=False)
    amount_paid = Column(Float, default=0.0)
    issued_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
