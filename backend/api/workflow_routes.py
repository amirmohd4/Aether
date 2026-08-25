from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from backend.database import get_db  # <-- FIXED
from backend.services.workflow_service import workflow_engine
from backend.services.fraud_service import fraud_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/start")
async def start_workflow(property_data: Dict[str, Any]):
    """Start a new workflow for property registration"""
    try:
        property_id = property_data.get("property_id", "unknown")
        workflow = workflow_engine.create_workflow(property_id, property_data)
        return {"status": "success", "workflow": workflow}
    except Exception as e:
        logger.error(f"Workflow start error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/advance")
async def advance_workflow(workflow_id: str, step: str, result: Dict[str, Any]):
    """Advance workflow to next step"""
    try:
        mock_workflow = {
            "workflow_id": workflow_id,
            "steps": {step: {"status": "pending"} for step in workflow_engine.steps},
            "status": "in_progress",
            "updated_at": None
        }
        updated = workflow_engine.advance_step(mock_workflow, step, result)
        return {"status": "success", "workflow": updated}
    except Exception as e:
        logger.error(f"Workflow advance error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get workflow status by ID"""
    return {
        "workflow_id": workflow_id,
        "status": "in_progress",
        "message": "Workflow retrieval not fully implemented"
    }

@router.post("/{workflow_id}/fraud-check")
async def check_fraud(workflow_id: str, property_data: Dict[str, Any]):
    """Run fraud detection on the property"""
    try:
        result = fraud_service.detect_fraud(property_data)
        return {"status": "success", "fraud_check": result}
    except Exception as e:
        logger.error(f"Fraud check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
