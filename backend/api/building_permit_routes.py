from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.building_permit import BuildingPermit

router = APIRouter(prefix="/building-permit", tags=["Building Permit"])

@router.post("/apply")
async def apply_building_permit(data: dict, db: Session = Depends(get_db)):
    property_id = data.get("property_id")
    developer_id = data.get("developer_id", "DEV-DEMO")
    project_name = data.get("project_name")
    project_type = data.get("project_type")
    plan_url = data.get("plan_url")

    if not property_id or not project_name:
        raise HTTPException(status_code=400, detail="property_id and project_name required")

    permit_id = f"BP-{uuid.uuid4().hex[:8].upper()}"

    new_permit = BuildingPermit(
        id=permit_id,
        property_id=property_id,
        developer_id=developer_id,
        project_name=project_name,
        project_type=project_type,
        plan_url=plan_url,
        status="applied",
        nocs={"fire": "pending", "municipal": "pending", "water": "pending"}
    )
    db.add(new_permit)
    db.commit()
    db.refresh(new_permit)

    return {
        "permit_id": permit_id,
        "status": "applied",
        "nocs": new_permit.nocs,
        "message": "Building permit application submitted."
    }

@router.get("/status/{permit_id}")
async def get_building_permit_status(permit_id: str, db: Session = Depends(get_db)):
    permit = db.query(BuildingPermit).filter(BuildingPermit.id == permit_id).first()
    if not permit:
        raise HTTPException(status_code=404, detail="Permit not found")
    return {
        "permit_id": permit.id,
        "status": permit.status,
        "nocs": permit.nocs,
        "scrutiny_score": permit.scrutiny_score,
        "scrutiny_issues": permit.scrutiny_issues,
        "fee_paid": permit.fee_paid,
        "issued_at": permit.issued_at
    }
