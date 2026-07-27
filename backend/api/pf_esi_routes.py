from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.pf_esi import PFESIRegistration

router = APIRouter(prefix="/pf-esi", tags=["PF/ESI Registration"])


@router.post("/apply")
async def apply_pf_esi(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    employer_name = data.get("employer_name")
    establishment_name = data.get("establishment_name")
    registration_type = data.get("registration_type")  # pf or esi
    employee_count = data.get("employee_count", 0)
    wage_ceiling = data.get("wage_ceiling", 0.0)

    if not citizen_id or not employer_name:
        raise HTTPException(status_code=400, detail="citizen_id and employer_name required")

    reg_id = f"PE-{uuid.uuid4().hex[:8].upper()}"
    new_reg = PFESIRegistration(
        id=reg_id,
        citizen_id=citizen_id,
        employer_name=employer_name,
        establishment_name=establishment_name,
        registration_type=registration_type,
        employee_count=employee_count,
        wage_ceiling=wage_ceiling,
        status="applied",
    )
    db.add(new_reg)
    db.commit()
    db.refresh(new_reg)

    return {
        "registration_id": reg_id,
        "status": "applied",
        "message": f"{registration_type.upper()} registration application submitted",
    }


@router.get("/status/{registration_id}")
async def get_pf_esi_status(registration_id: str, db: Session = Depends(get_db)):
    reg = db.query(PFESIRegistration).filter(PFESIRegistration.id == registration_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")
    return {
        "registration_id": reg.id,
        "employer_name": reg.employer_name,
        "registration_type": reg.registration_type,
        "status": reg.status,
        "fee_paid": reg.fee_paid,
        "issued_at": reg.issued_at,
        "expires_at": reg.expires_at,
    }
