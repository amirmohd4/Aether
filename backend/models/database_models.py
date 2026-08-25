from datetime import datetime
from typing import Optional
import enum

class WorkflowStatusEnum(str, enum.Enum):
    INITIATED = "initiated"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class FraudSeverityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Property:
    """Property model"""
    def __init__(self, property_id: str, owner_name: str, property_value: float, 
                 area_sqft: float, address: str, state: str):
        self.property_id = property_id
        self.owner_name = owner_name
        self.property_value = property_value
        self.area_sqft = area_sqft
        self.address = address
        self.state = state
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class WorkflowState:
    """Workflow state model"""
    def __init__(self, workflow_id: str, property_id: str, status: WorkflowStatusEnum):
        self.workflow_id = workflow_id
        self.property_id = property_id
        self.status = status
        self.current_step = None
        self.steps = {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class FraudDetectionLog:
    """Fraud detection log model"""
    def __init__(self, property_id: str, is_fraud: bool, score: float, severity: FraudSeverityEnum):
        self.property_id = property_id
        self.is_fraud = is_fraud
        self.score = score
        self.severity = severity
        self.detected_at = datetime.now()
        self.checks = []
