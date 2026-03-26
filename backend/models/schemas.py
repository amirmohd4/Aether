from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class WorkflowStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    rejected = "rejected"
    manual_review = "manual_review"

class FraudSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

# Property Schemas
class PropertyBase(BaseModel):
    property_id: str
    state: str
    location: str
    district: str
    owner: str
    title_status: str
    property_value: float
    property_size: float
    property_type: str

class PropertyResponse(PropertyBase):
    tehsil: Optional[str] = None
    village: Optional[str] = None
    owner_citizen_id: Optional[str] = None
    encumbrances: Optional[List[Dict[str, Any]]] = []
    history: Optional[List[Dict[str, Any]]] = []
    state_specific_data: Optional[Dict[str, Any]] = {}
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Citizen Schemas
class CitizenBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    aadhaar_number: str

class CitizenResponse(CitizenBase):
    citizen_id: str
    state: str
    district: str
    verified_attributes: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Certificate Schemas
class CertificateResponse(BaseModel):
    certificate_id: str
    certificate_type: str
    citizen_id: str
    issuing_authority: str
    status: str
    issue_date: Optional[datetime] = None
    state: str
    certificate_data: Dict[str, Any]
    
    class Config:
        from_attributes = True

# Workflow Schemas
class WorkflowStartRequest(BaseModel):
    property_id: str
    citizen_id: str
    workflow_type: str = "property_registration"

class WorkflowStepInfo(BaseModel):
    step_name: str
    status: str
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None

class WorkflowResponse(BaseModel):
    workflow_id: str
    property_id: str
    citizen_id: str
    workflow_type: str
    current_step: str
    status: WorkflowStatus
    steps_completed: List[Dict[str, Any]]
    steps_pending: List[Dict[str, Any]]
    failure_reason: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Fraud Detection Schemas
class FraudAlertResponse(BaseModel):
    fraud_id: str
    property_id: Optional[str] = None
    workflow_id: Optional[str] = None
    fraud_type: str
    severity: FraudSeverity
    fraud_score: float
    description: str
    explanation: str
    evidence: Dict[str, Any]
    flagged_at: datetime
    resolved: bool
    
    class Config:
        from_attributes = True

# API Key Schemas
class ApiKeyCreate(BaseModel):
    owner: str
    description: str
    rate_limit: int = 100

class ApiKeyResponse(BaseModel):
    key_id: str
    api_key: str
    owner: str
    description: str
    rate_limit: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
