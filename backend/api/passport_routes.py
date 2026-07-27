from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.passport_application import PassportApplication

router = APIRouter(prefix="/passport", tags=["Passport Application"])


@router.post("/apply")
async def apply_passport(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    applicant_name = data.get("applicant_name")
    passport_type = data.get("passport_type", "fresh")
    date_of_birth = data.get("date_of_birth")
    place_of_birth = data.get("place_of_birth")
    address = data.get("address")
    district = data.get("district")
    state = data.get("state")
    aadhaar_number = data.get("aadhaar_number")
    purpose = data.get("purpose")
    travel_country = data.get("travel_country")

    if not citizen_id or not applicant_name:
        raise HTTPException(status_code=400, detail="citizen_id and applicant_name required")

    passport_id = f"PPT-{uuid.uuid4().hex[:8].upper()}"
    parsed_dob = None
    if date_of_birth:
        try:
            parsed_dob = datetime.fromisoformat(date_of_birth.replace("Z", ""))
        except Exception:
            parsed_dob = None

    new_passport = PassportApplication(
        id=passport_id,
        citizen_id=citizen_id,
        applicant_name=applicant_name,
        passport_type=passport_type,
        date_of_birth=parsed_dob,
        place_of_birth=place_of_birth,
        address=address,
        district=district,
        state=state,
        aadhaar_number=aadhaar_number,
        purpose=purpose,
        travel_country=travel_country,
        status="applied",
    )
    db.add(new_passport)
    db.commit()
    db.refresh(new_passport)

    return {
        "application_id": passport_id,
        "status": "applied",
        "message": "Passport application submitted",
    }


@router.get("/status/{application_id}")
async def get_passport_status(application_id: str, db: Session = Depends(get_db)):
    passport = db.query(PassportApplication).filter(PassportApplication.id == application_id).first()
    if not passport:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "application_id": passport.id,
        "applicant_name": passport.applicant_name,
        "passport_type": passport.passport_type,
        "status": passport.status,
        "passport_number": passport.passport_number,
        "fee_paid": passport.fee_paid,
        "issued_at": passport.issued_at,
        "expires_at": passport.expires_at,
    }
