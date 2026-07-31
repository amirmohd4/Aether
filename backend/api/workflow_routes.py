from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models.database_models import WorkflowState, WorkflowStatusEnum

router = APIRouter(prefix="/workflow", tags=["workflow"])

class WorkflowStartRequest(BaseModel):
    service_id: str
    country: str
    state: str
    national_id: str
    property_id: Optional[str] = None
    citizen_id: Optional[str] = None

@router.post("/start")
async def start_workflow(request: WorkflowStartRequest):
    db = SessionLocal()
    try:
        workflow_id = f"wf-{uuid.uuid4().hex[:8]}"
        workflow = WorkflowState(
            workflow_id=workflow_id,
            property_id=request.property_id,
            citizen_id=request.citizen_id,
            workflow_type=request.service_id,
            current_step="started",
            status=WorkflowStatusEnum.in_progress,
            steps_completed=[],
            steps_pending=[],
            started_at=datetime.utcnow(),
            workflow_metadata={
                "country": request.country,
                "state": request.state,
                "national_id": request.national_id
            }
        )
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        return {
            "workflow_id": workflow_id,
            "status": "started",
            "current_step": "title_verification",
            "message": "Workflow started successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get("/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    db = SessionLocal()
    try:
        workflow = db.query(WorkflowState).filter(WorkflowState.workflow_id == workflow_id).first()
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return {
            "workflow_id": workflow.workflow_id,
            "status": workflow.status.value if workflow.status else "unknown",
            "current_step": workflow.current_step,
            "progress_percentage": len(workflow.steps_completed or []) / max(1, len(workflow.steps_pending or []) + len(workflow.steps_completed or [])) * 100
        }
    finally:
        db.close()
