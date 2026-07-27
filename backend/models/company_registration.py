from sqlalchemy import Column, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime


class CompanyRegistration(Base):
    __tablename__ = "company_registrations"

    id = Column(String, primary_key=True)
    citizen_id = Column(String, index=True)
    company_name = Column(String)
    company_type = Column(String)  # private_limited, public_limited, opc, llp
    cin = Column(String, nullable=True)
    authorised_capital = Column(Float, default=0.0)
    paid_up_capital = Column(Float, default=0.0)
    directors = Column(String)  # comma separated names
    registered_office = Column(String)
    state = Column(String)
    status = Column(String)  # applied, approved, rejected
    fee_paid = Column(Boolean, default=False)
    amount_paid = Column(Float, default=0.0)
    issued_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
