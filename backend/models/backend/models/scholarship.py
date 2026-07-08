from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime

class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(String, primary_key=True)
    student_name = Column(String)
    citizen_id = Column(String, index=True)
    income = Column(Float)
    caste = Column(String)
    marks = Column(Float)
    college_id = Column(String)
    course = Column(String)
    status = Column(String)  # applied, approved, rejected, disbursed
    amount = Column(Float, default=0.0)
    fee_paid = Column(Boolean, default=False)
    disbursed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
