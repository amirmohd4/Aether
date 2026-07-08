from sqlalchemy import Column, String, DateTime, Boolean
from database import Base
from datetime import datetime

class DeathCertificate(Base):
    __tablename__ = "death_certificates"

    id = Column(String, primary_key=True)
    deceased_name = Column(String)
    citizen_id = Column(String, index=True)
    hospital_id = Column(String)
    date_of_death = Column(DateTime)
    cause_of_death = Column(String)
    status = Column(String)  # applied, issued, delivered
    issued_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
