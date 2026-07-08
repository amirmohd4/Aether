from sqlalchemy import Column, String, DateTime, Boolean
from database import Base
from datetime import datetime

class Admission(Base):
    __tablename__ = "admissions"

    id = Column(String, primary_key=True)
    student_name = Column(String)
    citizen_id = Column(String, index=True)
    school_id = Column(String)
    class_grade = Column(String)
    admission_year = Column(String)
    status = Column(String)  # applied, approved, rejected, enrolled
    fee_paid = Column(Boolean, default=False)
    enrolled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
