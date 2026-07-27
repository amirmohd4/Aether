from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.affordable_housing import AffordableHousing

router = APIRouter(prefix="/housing", tags=["Affordable Housing"])


@router.post("/apply")
async def apply_affordable_housing(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    applicant_name = data.get("applicant_name")
    address = data.get("address")
    district = data.get("district")
    state = data.get("state")
    annual_income = data.get("annual_income", 0.0)
    family_size = data.get("family_size", 0)
    preferred_tenant_type = data.get("preferred_tenant_type", "ownership")
    monthly_rent_affordable = data.get("monthly_rent_affordable", 0.0)

    if not citizen_id or not applicant_name:
        raise HTTPException(status_code=400, detail="citizen_id and applicant_name required")

    housing_id = f"HSG-{uuid.uuid4().hex[:8].upper()}"
    new_app = AffordableHousing(
        id=housing_id,
        citizen_id=citizen_id,
        applicant_name=applicant_name,
        address=address,
        district=district,
        state=state,
        annual_income=annual_income,
        family_size=family_size,
        preferred_tenant_type=preferred_tenant_type,
        monthly_rent_affordable=monthly_rent_affordable,
        status="applied",
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    return {
        "application_id": housing_id,
        "status": "applied",
        "message": "Affordable housing application submitted",
    }


@router.get("/status/{application_id}")
async def get_affordable_housing_status(application_id: str, db: Session = Depends(get_db)):
    app = db.query(AffordableHousing).filter(AffordableHousing.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "application_id": app.id,
        "applicant_name": app.applicant_name,
        "status": app.status,
        "allotted_at": app.allotted_at,
    }
