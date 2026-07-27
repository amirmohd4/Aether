from sqlalchemy import Column, String, DateTime, Boolean, JSON
from database import Base
from datetime import datetime


class FIRReport(Base):
    __tablename__ = "fir_reports"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    complainant_name = Column(String)
    accused_name = Column(String, nullable=True)
    incident_date = Column(DateTime)
    incident_location = Column(String)
    police_station = Column(String)
    district = Column(String)
    state = Column(String)
    fir_sections = Column(String)  # IPC sections
    description = Column(String)
    status = Column(String)  # filed, under_investigation, closed
    evidence = Column(JSON, default=[])
    filed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
