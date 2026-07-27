from sqlalchemy import Column, String, DateTime, Boolean, JSON
from database import Base
from datetime import datetime


class ECourt(Base):
    __tablename__ = "e_courts"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    case_number = Column(String)
    court_name = Column(String)
    petitioner = Column(String)
    respondent = Column(String)
    hearing_date = Column(DateTime, nullable=True)
    status = Column(String)  # scheduled, adjourned, completed
    documents = Column(JSON, default=[])
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
