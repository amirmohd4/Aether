from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

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
    title_status = Column(String)  # clear, disputed, encumbered
    encumbrances = Column(JSON)  # List of encumbrances
    history = Column(JSON)  # Property transaction history
    property_value = Column(Float)
    property_size = Column(Float)
    property_type = Column(String)  # residential, commercial, agricultural
    state_specific_data = Column(JSON)  # JSONB for state-specific fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner_citizen = relationship("Citizen", back_populates="properties")
    workflow_states = relationship("WorkflowState", back_populates="property")
    fraud_logs = relationship("FraudDetectionLog", back_populates="property")


class Certificate(Base):
    __tablename__ = "certificates"
    
    certificate_id = Column(String, primary_key=True, index=True)
    certificate_type = Column(String)  # birth, death, caste, income, residence
    citizen_id = Column(String, ForeignKey("citizens.citizen_id"))
    issuing_authority = Column(String)
    status = Column(String)  # pending, issued, rejected
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime, nullable=True)
    state = Column(String)
    certificate_data = Column(JSON)  # Certificate specific data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    citizen = relationship("Citizen", back_populates="certificates")


class Citizen(Base):
    __tablename__ = "citizens"
    
    citizen_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    aadhaar_number = Column(String, unique=True, index=True)
    verified_attributes = Column(JSON)  # Dict of verified attributes
    state = Column(String)
    district = Column(String)
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    properties = relationship("Property", back_populates="owner_citizen")
    certificates = relationship("Certificate", back_populates="citizen")
    workflow_states = relationship("WorkflowState", back_populates="citizen")


class WorkflowStatusEnum(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    rejected = "rejected"
    manual_review = "manual_review"


class WorkflowState(Base):
    __tablename__ = "workflow_states"
    
    workflow_id = Column(String, primary_key=True, index=True)
    property_id = Column(String, ForeignKey("properties.property_id"))
    citizen_id = Column(String, ForeignKey("citizens.citizen_id"))
    workflow_type = Column(String)  # property_registration, certificate_request
    current_step = Column(String)
    status = Column(Enum(WorkflowStatusEnum))
    steps_completed = Column(JSON)  # List of completed steps with timestamps
    steps_pending = Column(JSON)  # List of pending steps
    failure_reason = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    workflow_metadata = Column(JSON)  # Additional workflow data
    
    # Relationships
    property = relationship("Property", back_populates="workflow_states")
    citizen = relationship("Citizen", back_populates="workflow_states")
    fraud_logs = relationship("FraudDetectionLog", back_populates="workflow")


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
    fraud_score = Column(Float)  # 0-100
    description = Column(Text)
    explanation = Column(Text)  # AI explanation
    evidence = Column(JSON)  # Evidence data
    flagged_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    
    # Relationships
    property = relationship("Property", back_populates="fraud_logs")
    workflow = relationship("WorkflowState", back_populates="fraud_logs")


class ApiKey(Base):
    __tablename__ = "api_keys"
    
    key_id = Column(String, primary_key=True, index=True)
    api_key = Column(String, unique=True, index=True)
    owner = Column(String)
    description = Column(String)
    rate_limit = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0)
