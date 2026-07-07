from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import SessionLocal
from models.database_models import Property, WorkflowState, WorkflowStatusEnum

router = APIRouter(prefix="/developer", tags=["Developer"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/building-permit")
async def apply_building_permit(
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Developer submits building plan → auto‑route to Fire, Pollution, Municipal.
    """
    property_id = data.get("property_id")
    plan_url = data.get("plan_url")
    developer_id = data.get("developer_id", "DEV-DEMO")
    
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
        citizen_id=developer_id,  # reuse citizen_id as developer id
        workflow_type="building_permit",
        current_step="NOC Collection",
        status=WorkflowStatusEnum.in_progress,
        steps_completed=[],
        steps_pending=["Fire NOC", "Pollution NOC", "Municipal NOC", "Water NOC"],
        started_at=datetime.utcnow(),
        workflow_metadata={"plan_url": plan_url}
    )
    db.add(new_workflow)
    db.commit()
    db.refresh(new_workflow)
    
    return {
        "application_id": workflow_id,
        "status": "in_progress",
        "departments": ["Fire", "Pollution", "Municipal", "Water"],
        "message": "Building permit application submitted. All NOCs requested."
    }

@router.post("/land-conversion")
async def convert_land_use(
    data: dict,
    db: Session = Depends(get_db)
):
    """Developer requests land use conversion."""
    property_id = data.get("property_id")
    target_use = data.get("target_use")
    
    if not property_id or not target_use:
        raise HTTPException(status_code=400, detail="property_id and target_use required")
    
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Simulate conversion fee calculation
    conversion_fee = prop.property_value * 0.02  # 2% of property value
    
    return {
        "property_id": property_id,
        "current_use": prop.property_type,
        "target_use": target_use,
        "conversion_fee": conversion_fee,
        "status": "pending",
        "message": "Land conversion request received. Under review."
    }

@router.get("/compliance/{property_id}")
async def check_compliance(
    property_id: str,
    db: Session = Depends(get_db)
):
    """Check if property complies with all regulations."""
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Simulate compliance checks
    checks = {
        "zoning": "approved",
        "environmental": "approved",
        "fire_safety": "approved",
        "building_codes": "approved"
    }
    return {
        "property_id": property_id,
        "compliance": checks,
        "overall_status": "compliant"
    }
