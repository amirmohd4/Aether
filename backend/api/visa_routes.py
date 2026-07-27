from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.visa_service import VisaService

router = APIRouter(prefix="/visa", tags=["Visa Services"])


@router.post("/apply")
async def apply_visa(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    applicant_name = data.get("applicant_name")
    passport_number = data.get("passport_number")
    visa_type = data.get("visa_type")  # tourist, business, student, work, transit
    destination_country = data.get("destination_country")
    duration_days = data.get("duration_days", 30)
    purpose = data.get("purpose")
    entry_type = data.get("entry_type", "single")

    if not citizen_id or not applicant_name or not passport_number:
        raise HTTPException(status_code=400, detail="citizen_id, applicant_name and passport_number required")

    visa_id = f"VSA-{uuid.uuid4().hex[:8].upper()}"
    new_visa = VisaService(
        id=visa_id,
        citizen_id=citizen_id,
        applicant_name=applicant_name,
        passport_number=passport_number,
        visa_type=visa_type,
        destination_country=destination_country,
        duration_days=duration_days,
        purpose=purpose,
        entry_type=entry_type,
        status="applied",
    )
    db.add(new_visa)
    db.commit()
    db.refresh(new_visa)

    return {
        "application_id": visa_id,
        "status": "applied",
        "message": "Visa application submitted",
    }


@router.get("/status/{application_id}")
async def get_visa_status(application_id: str, db: Session = Depends(get_db)):
    visa = db.query(VisaService).filter(VisaService.id == application_id).first()
    if not visa:
        raise HTTPException(status_code=404, detail="Visa application not found")
    return {
        "application_id": visa.id,
        "applicant_name": visa.applicant_name,
        "visa_type": visa.visa_type,
        "destination_country": visa.destination_country,
        "status": visa.status,
        "visa_number": visa.visa_number,
        "fee_paid": visa.fee_paid,
        "issued_at": visa.issued_at,
        "expires_at": visa.expires_at,
    }
