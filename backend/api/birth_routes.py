from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.birth_certificate import BirthCertificate

router = APIRouter(prefix="/birth", tags=["Birth Certificate"])

@router.post("/register")
async def register_birth(data: dict, db: Session = Depends(get_db)):
    child_name = data.get("child_name")
    father_name = data.get("father_name")
    mother_name = data.get("mother_name")
    hospital_id = data.get("hospital_id")
    date_of_birth = data.get("date_of_birth")
    gender = data.get("gender")
    citizen_id = data.get("citizen_id")

    if not child_name or not father_name:
        raise HTTPException(status_code=400, detail="child_name and father_name required")

    cert_id = f"BC-{uuid.uuid4().hex[:8].upper()}"
    new_cert = BirthCertificate(
        id=cert_id,
        child_name=child_name,
        father_name=father_name,
        mother_name=mother_name,
        hospital_id=hospital_id,
        date_of_birth=date_of_birth,
        gender=gender,
        citizen_id=citizen_id,
        status="applied"
    )
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    return {"certificate_id": cert_id, "status": "applied", "message": "Birth registered"}

@router.get("/status/{certificate_id}")
async def get_birth_status(certificate_id: str, db: Session = Depends(get_db)):
    cert = db.query(BirthCertificate).filter(BirthCertificate.id == certificate_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return {
        "certificate_id": cert.id,
        "child_name": cert.child_name,
        "status": cert.status,
        "issued_at": cert.issued_at
    }
