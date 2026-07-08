from sqlalchemy import Column, String, DateTime, Boolean
from database import Base
from datetime import datetime

class TransferCertificate(Base):
    __tablename__ = "transfer_certificates"

    id = Column(String, primary_key=True)
    student_name = Column(String)
    citizen_id = Column(String, index=True)
    from_school = Column(String)
    to_school = Column(String)
    reason = Column(String)
    status = Column(String)  # applied, approved, rejected, issued
    issued_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
