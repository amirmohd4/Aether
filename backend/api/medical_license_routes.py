from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.medical_license import MedicalLicense

router = APIRouter(prefix="/medical-license", tags=["Medical License"])

@router.post("/apply")
async def apply_medical_license(data: dict, db: Session = Depends(get_db)):
    doctor_name = data.get("doctor_name")
    doctor_id = data.get("doctor_id")
    qualification = data.get("qualification")
    institution = data.get("institution")

    if not doctor_name or not qualification:
        raise HTTPException(status_code=400, detail="doctor_name and qualification required")

    license_id = f"ML-{uuid.uuid4().hex[:8].upper()}"
    new_license = MedicalLicense(
        id=license_id,
        doctor_name=doctor_name,
        doctor_id=doctor_id,
        qualification=qualification,
        institution=institution,
        status="applied"
    )
    db.add(new_license)
    db.commit()
    db.refresh(new_license)
    return {"license_id": license_id, "status": "applied", "message": "Medical license application submitted"}

@router.get("/status/{license_id}")
async def get_medical_license_status(license_id: str, db: Session = Depends(get_db)):
    lic = db.query(MedicalLicense).filter(MedicalLicense.id == license_id).first()
    if not lic:
        raise HTTPException(status_code=404, detail="License not found")
    return {
        "license_id": lic.id,
        "doctor_name": lic.doctor_name,
        "status": lic.status,
        "fee_paid": lic.fee_paid,
        "issued_at": lic.issued_at,
        "expires_at": lic.expires_at
    }
