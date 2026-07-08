from sqlalchemy import Column, String, DateTime, Boolean, JSON
from database import Base
from datetime import datetime

class BirthCertificate(Base):
    __tablename__ = "birth_certificates"

    id = Column(String, primary_key=True)
    child_name = Column(String)
    father_name = Column(String)
    mother_name = Column(String)
    hospital_id = Column(String)
    date_of_birth = Column(DateTime)
    gender = Column(String)
    citizen_id = Column(String, index=True)  # child's Aadhaar after generation
    status = Column(String)  # applied, issued, delivered
    issued_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
