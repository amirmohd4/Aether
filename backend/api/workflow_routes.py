from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from database import SessionLocal
from models.database_models import Property, WorkflowState, WorkflowStatusEnum

router = APIRouter(prefix="/workflow", tags=["Workflow"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/start")
async def start_workflow(
    data: dict,
    db: Session = Depends(get_db)
):
    """Start a new workflow for a property"""
    property_id = data.get("property_id")
    citizen_id = data.get("citizen_id", "CIT-DEMO-001")
    workflow_type = data.get("workflow_type", "property_registration")
    
    if not property_id:
        raise HTTPException(status_code=400, detail="property_id is required")
    
    # Check if property exists
    property = db.query(Property).filter(Property.property_id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail=f"Property {property_id} not found")
    
    # Check if there's already an active workflow
    existing = db.query(WorkflowState).filter(
        WorkflowState.property_id == property_id,
        WorkflowState.status == WorkflowStatusEnum.in_progress
    ).first()
    
    if existing:
        return {
            "workflow_id": existing.workflow_id,
            "status": existing.status.value,
            "current_step": existing.current_step,
            "progress_percentage": 25,
            "message": "Workflow already in progress"
        }
    
    # Create new workflow
    workflow_id = f"WF-{uuid.uuid4().hex[:12].upper()}"
    
    new_workflow = WorkflowState(
        workflow_id=workflow_id,
        property_id=property_id,
        citizen_id=citizen_id,
        workflow_type=workflow_type,
        current_step="Title Verification",
        status=WorkflowStatusEnum.in_progress,
        steps_completed=[],
        steps_pending=["Title Verification", "Encumbrance Check", "Stamp Duty", "Payment", "Registration", "Mutation"],
        started_at=datetime.utcnow(),
        workflow_metadata={"property_value": property.property_value}
    )
    
    db.add(new_workflow)
    db.commit()
    db.refresh(new_workflow)
    
    return {
        "workflow_id": workflow_id,
        "status": "in_progress",
        "current_step": "Title Verification",
        "progress_percentage": 10,
        "message": "Workflow started successfully"
    }

@router.get("/{workflow_id}")
async def get_workflow_status(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """Get workflow status"""
    workflow = db.query(WorkflowState).filter(WorkflowState.workflow_id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Calculate progress (simplified)
    total_steps = len(workflow.steps_pending or []) + len(workflow.steps_completed or [])
    completed = len(workflow.steps_completed or [])
    progress = int((completed / total_steps) * 100) if total_steps > 0 else 0
    
    return {
        "workflow_id": workflow.workflow_id,
        "status": workflow.status.value,
        "current_step": workflow.current_step,
        "progress_percentage": progress,
        "steps_completed": workflow.steps_completed or [],
        "steps_pending": workflow.steps_pending or [],
        "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
        "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None
    }
