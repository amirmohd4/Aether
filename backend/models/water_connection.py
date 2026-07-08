from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime

class WaterConnection(Base):
    __tablename__ = "water_connections"

    id = Column(String, primary_key=True)
    property_id = Column(String, index=True)
    citizen_id = Column(String, index=True)
    connection_type = Column(String)  # residential, commercial, industrial
    status = Column(String)  # applied, approved, connected, rejected
    fee_paid = Column(Boolean, default=False)
    amount_paid = Column(Float, default=0.0)
    connected_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
