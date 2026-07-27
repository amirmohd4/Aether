from sqlalchemy import Column, String, DateTime, Boolean, JSON
from database import Base
from datetime import datetime


class CourtCaseFiling(Base):
    __tablename__ = "court_case_filings"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    petitioner_name = Column(String)
    respondent_name = Column(String)
    case_type = Column(String)  # civil, criminal, family, property
    court_name = Column(String)
    district = Column(String)
    state = Column(String)
    subject = Column(String)
    description = Column(String)
    documents = Column(JSON, default=[])
    status = Column(String)  # filed, under_hearing, disposed, dismissed
    case_number = Column(String, nullable=True)
    next_hearing = Column(DateTime, nullable=True)
    filed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
