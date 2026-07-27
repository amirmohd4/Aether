from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.pmay_application import PMAYApplication

router = APIRouter(prefix="/pmay", tags=["PMAY Application"])


@router.post("/apply")
async def apply_pmay(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    applicant_name = data.get("applicant_name")
    spouse_name = data.get("spouse_name")
    address = data.get("address")
    district = data.get("district")
    state = data.get("state")
    annual_income = data.get("annual_income", 0.0)
    category = data.get("category")  # EWS, LIG, MIG_I, MIG_II
    carpet_area_required = data.get("carpet_area_required", 0.0)
    aadhaar_number = data.get("aadhaar_number")

    if not citizen_id or not applicant_name:
        raise HTTPException(status_code=400, detail="citizen_id and applicant_name required")

    pmay_id = f"PMAY-{uuid.uuid4().hex[:8].upper()}"
    new_app = PMAYApplication(
        id=pmay_id,
        citizen_id=citizen_id,
        applicant_name=applicant_name,
        spouse_name=spouse_name,
        address=address,
        district=district,
        state=state,
        annual_income=annual_income,
        category=category,
        carpet_area_required=carpet_area_required,
        aadhaar_number=aadhaar_number,
        status="applied",
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    return {
        "application_id": pmay_id,
        "status": "applied",
        "message": "PMAY application submitted",
    }


@router.get("/status/{application_id}")
async def get_pmay_status(application_id: str, db: Session = Depends(get_db)):
    app = db.query(PMAYApplication).filter(PMAYApplication.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "application_id": app.id,
        "applicant_name": app.applicant_name,
        "category": app.category,
        "status": app.status,
        "subsidy_amount": app.subsidy_amount,
        "sanctioned_at": app.sanctioned_at,
    }
