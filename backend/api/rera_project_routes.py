from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.rera_project import RERAProject

router = APIRouter(prefix="/rera-project", tags=["RERA Project Registration"])


@router.post("/apply")
async def apply_rera_project(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    developer_name = data.get("developer_name")
    project_name = data.get("project_name")
    project_type = data.get("project_type")
    project_address = data.get("project_address")
    district = data.get("district")
    state = data.get("state")
    land_area = data.get("land_area", 0.0)
    total_units = data.get("total_units", 0)
    estimated_cost = data.get("estimated_cost", 0.0)
    completion_date = data.get("completion_date")

    if not citizen_id or not project_name:
        raise HTTPException(status_code=400, detail="citizen_id and project_name required")

    project_id = f"RERA-P-{uuid.uuid4().hex[:8].upper()}"
    parsed_completion = None
    if completion_date:
        try:
            parsed_completion = datetime.fromisoformat(completion_date.replace("Z", ""))
        except Exception:
            parsed_completion = None

    new_project = RERAProject(
        id=project_id,
        citizen_id=citizen_id,
        developer_name=developer_name,
        project_name=project_name,
        project_type=project_type,
        project_address=project_address,
        district=district,
        state=state,
        land_area=land_area,
        total_units=total_units,
        estimated_cost=estimated_cost,
        completion_date=parsed_completion,
        status="applied",
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "project_id": project_id,
        "status": "applied",
        "message": "RERA project registration submitted",
    }


@router.get("/status/{project_id}")
async def get_rera_project_status(project_id: str, db: Session = Depends(get_db)):
    project = db.query(RERAProject).filter(RERAProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "project_id": project.id,
        "project_name": project.project_name,
        "developer_name": project.developer_name,
        "status": project.status,
        "rera_number": project.rera_number,
        "fee_paid": project.fee_paid,
        "issued_at": project.issued_at,
    }
