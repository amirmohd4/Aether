from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.models.database_models import WorkflowState, WorkflowStatusEnum, Property
from backend.services.connector_services import connector_service
import uuid
import logging

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """
    Workflow engine for property registration
    Steps: title verification → encumbrance check → stamp duty → payment → registration → mutation
    """

    def __init__(self):
        self.steps = [
            "title_verification",
            "encumbrance_check", 
            "stamp_duty",
            "payment",
            "registration",
            "mutation"
        ]

    def create_workflow(self, property_id: str, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new workflow for property registration"""
        workflow_id = str(uuid.uuid4())
        return {
            "workflow_id": workflow_id,
            "property_id": property_id,
            "status": "initiated",
            "current_step": self.steps[0],
            "steps": {step: {"status": "pending", "completed_at": None} for step in self.steps},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

    def advance_step(self, workflow: Dict[str, Any], step: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Advance workflow to next step"""
        if step not in workflow["steps"]:
            raise ValueError(f"Invalid step: {step}")
        
        workflow["steps"][step]["status"] = "completed"
        workflow["steps"][step]["result"] = result
        workflow["steps"][step]["completed_at"] = datetime.now().isoformat()
        workflow["updated_at"] = datetime.now().isoformat()

        # Move to next step
        current_index = self.steps.index(step)
        if current_index + 1 < len(self.steps):
            workflow["current_step"] = self.steps[current_index + 1]
            workflow["steps"][self.steps[current_index + 1]]["status"] = "in_progress"
        else:
            workflow["status"] = "completed"
            workflow["current_step"] = None

        return workflow

# Singleton instance
workflow_engine = WorkflowEngine()
