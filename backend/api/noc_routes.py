from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models.database_models import WorkflowState, WorkflowStatusEnum

router = APIRouter(prefix="/noc", tags=["NOC"])

# Configurable rules for auto‑approval
NOC_RULES = {
    "fire": {
        "auto_approve_if": lambda prop, plan: prop.property_type == "residential" and plan.get("height", 0) <= 15,
        "deemed_days": 14
    },
    "pollution": {
        "auto_approve_if": lambda prop, plan: prop.property_type in ["residential", "commercial"] and plan.get("emissions", 0) < 50,
        "deemed_days": 21
    },
    "municipal": {
        "auto_approve_if": lambda prop, plan: prop.property_type in ["residential", "commercial"],
        "deemed_days": 15
    },
    "water": {
        "auto_approve_if": lambda prop, plan: prop.property_type == "residential",
        "deemed_days": 10
    }
}

@router.post("/auto-approve/{workflow_id}")
async def auto_approve_noc(workflow_id: str, db: Session = Depends(get_db)):
    """
    Automatically approve NOCs based on rules.
    """
    workflow = db.query(WorkflowState).filter(WorkflowState.workflow_id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Get property from workflow
    property_id = workflow.property_id
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Get plan details from workflow_metadata (or assume default)
    plan_details = workflow.workflow_metadata.get("plan_details", {})
    
    approved_nocs = {}
    pending_nocs = {}
    for dept, rule in NOC_RULES.items():
        if rule["auto_approve_if"](prop, plan_details):
            approved_nocs[dept] = {
                "status": "auto_approved",
                "approved_at": datetime.utcnow().isoformat()
            }
        else:
            pending_nocs[dept] = {
                "status": "pending",
                "requested_at": datetime.utcnow().isoformat(),
                "deemed_approval_date": (datetime.utcnow() + timedelta(days=rule["deemed_days"])).isoformat()
            }
    
    # Update workflow_metadata with NOC status
    if not workflow.workflow_metadata:
        workflow.workflow_metadata = {}
    workflow.workflow_metadata["noc_requests"] = {
        "approved": approved_nocs,
        "pending": pending_nocs
    }
    db.commit()
    
    # If all NOCs approved, advance workflow
    all_approved = len(pending_nocs) == 0
    if all_approved:
        workflow.current_step = "NOC Collection Complete"
    else:
        workflow.current_step = "Waiting for NOCs"
    
    db.commit()
    
    return {
        "workflow_id": workflow_id,
        "auto_approved": approved_nocs,
        "pending": pending_nocs,
        "all_approved": all_approved
    }

@router.get("/deemed-approval/{workflow_id}")
async def check_deemed_approval(workflow_id: str, db: Session = Depends(get_db)):
    """
    Check if any pending NOC has crossed the deemed approval date.
    """
    workflow = db.query(WorkflowState).filter(WorkflowState.workflow_id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    noc_data = workflow.workflow_metadata.get("noc_requests", {})
    pending = noc_data.get("pending", {})
    now = datetime.utcnow()
    deemed_approved = []
    
    for dept, info in pending.items():
        deemed_date = datetime.fromisoformat(info.get("deemed_approval_date"))
        if now >= deemed_date:
            deemed_approved.append(dept)
            # Auto‑approve
            pending[dept]["status"] = "deemed_approved"
            pending[dept]["deemed_approved_at"] = now.isoformat()
    
    if deemed_approved:
        # Update workflow
        workflow.workflow_metadata["noc_requests"]["pending"] = pending
        workflow.current_step = "NOC Collection Complete"
        db.commit()
    
    return {
        "workflow_id": workflow_id,
        "deemed_approved": deemed_approved,
        "pending_nocs": pending
    }
