from ..database import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

# ============ CITIZEN ============
class Citizen(Base):
    __tablename__ = "citizens"
    citizen_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    aadhaar_number = Column(String, unique=True, index=True)
    verified_attributes = Column(JSON)
    state = Column(String)
    district = Column(String)
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    properties = relationship("Property", back_populates="owner_citizen")
    certificates = relationship("Certificate", back_populates="citizen")
    workflow_states = relationship("WorkflowState", back_populates="citizen")

# ============ PROPERTY ============
class Property(Base):
    __tablename__ = "properties"
    property_id = Column(String, primary_key=True, index=True)
    state = Column(String, index=True)
    location = Column(String)
    district = Column(String)
    tehsil = Column(String)
    village = Column(String)
    owner = Column(String)
    owner_citizen_id = Column(String, ForeignKey("citizens.citizen_id"))
    title_status = Column(String)
    encumbrances = Column(JSON)
    history = Column(JSON)
    property_value = Column(Float)
    property_size = Column(Float)
    property_type = Column(String)
    state_specific_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner_citizen = relationship("Citizen", back_populates="properties")
    workflow_states = relationship("WorkflowState", back_populates="property")
    fraud_logs = relationship("FraudDetectionLog", back_populates="property")

# ============ CERTIFICATE ============
class Certificate(Base):
    __tablename__ = "certificates"
    certificate_id = Column(String, primary_key=True, index=True)
    certificate_type = Column(String)
    citizen_id = Column(String, ForeignKey("citizens.citizen_id"))
    issuing_authority = Column(String)
    status = Column(String)
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime, nullable=True)
    state = Column(String)
    certificate_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    citizen = relationship("Citizen", back_populates="certificates")

# ============ WORKFLOW ============
class WorkflowStatusEnum(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    rejected = "rejected"
    manual_review = "manual_review"

class WorkflowState(Base):
    __tablename__ = "workflow_states"
    workflow_id = Column(String, primary_key=True, index=True)
    property_id = Column(String, ForeignKey("properties.property_id"), nullable=True)
    citizen_id = Column(String, ForeignKey("citizens.citizen_id"), nullable=True)
    workflow_type = Column(String)
    current_step = Column(String)
    status = Column(Enum(WorkflowStatusEnum))
    steps_completed = Column(JSON)
    steps_pending = Column(JSON)
    failure_reason = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    workflow_metadata = Column(JSON)
    
    property = relationship("Property", back_populates="workflow_states")
    citizen = relationship("Citizen", back_populates="workflow_states")
    fraud_logs = relationship("FraudDetectionLog", back_populates="workflow")

# ============ FRAUD ============
class FraudSeverityEnum(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class FraudDetectionLog(Base):
    __tablename__ = "fraud_detection_logs"
    fraud_id = Column(String, primary_key=True, index=True)
    property_id = Column(String, ForeignKey("properties.property_id"), nullable=True)
    workflow_id = Column(String, ForeignKey("workflow_states.workflow_id"), nullable=True)
    fraud_type = Column(String)
    severity = Column(Enum(FraudSeverityEnum))
    fraud_score = Column(Float)
    description = Column(Text)
    explanation = Column(Text)
    evidence = Column(JSON)
    flagged_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    
    property = relationship("Property", back_populates="fraud_logs")
    workflow = relationship("WorkflowState", back_populates="fraud_logs")

# ============ API KEY ============
class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    owner = Column(String)
    rate_limit = Column(Integer, default=100)
    usage_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
