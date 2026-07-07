from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.database_models import Property, WorkflowState, WorkflowStatusEnum
from api.noc_routes import auto_approve_nocs

router = APIRouter(prefix="/developer", tags=["Developer"])

@router.post("/building-permit")
async def apply_building_permit(
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Developer submits building plan → auto‑route to Fire, Pollution, Municipal.
    Auto‑approves NOCs immediately after workflow creation.
    """
    property_id = data.get("property_id")
    plan_url = data.get("plan_url")
    developer_id = data.get("developer_id", "DEV-DEMO")
    plan_details = data.get("plan_details", {})  # { "height": 12, "emissions": 20, "built_up_area": 500, "setback": 4, "parking": 2 }
    
    if not property_id:
        raise HTTPException(status_code=400, detail="property_id required")
    
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Create a workflow for building permit
    workflow_id = f"BP-{uuid.uuid4().hex[:8].upper()}"
    new_workflow = WorkflowState(
        workflow_id=workflow_id,
        property_id=property_id,
        citizen_id=developer_id,
        workflow_type="building_permit",
        current_step="NOC Collection",
        status=WorkflowStatusEnum.in_progress,
        steps_completed=[],
        steps_pending=["Fire NOC", "Pollution NOC", "Municipal NOC", "Water NOC"],
        started_at=datetime.utcnow(),
        workflow_metadata={"plan_url": plan_url, "plan_details": plan_details}
    )
    db.add(new_workflow)
    db.commit()
    db.refresh(new_workflow)
    
    # Trigger NOC auto‑approval
    noc_result = auto_approve_nocs(new_workflow, db)
    
    return {
        "application_id": workflow_id,
        "status": "in_progress",
        "departments": ["Fire", "Pollution", "Municipal", "Water"],
        "noc_result": noc_result,
        "message": "Building permit application submitted. NOCs auto‑processed."
    }
