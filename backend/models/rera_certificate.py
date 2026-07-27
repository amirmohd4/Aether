from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime


class RERACertificate(Base):
    __tablename__ = "rera_certificates"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    project_name = Column(String)
    developer_name = Column(String)
    rera_number = Column(String, nullable=True)
    project_id = Column(String, nullable=True)
    certificate_type = Column(String)  # registration, extension, amendment
    status = Column(String)  # applied, issued, rejected
    fee_paid = Column(Boolean, default=False)
    amount_paid = Column(Float, default=0.0)
    issued_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
