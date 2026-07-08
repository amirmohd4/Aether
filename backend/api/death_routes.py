from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.death_certificate import DeathCertificate

router = APIRouter(prefix="/death", tags=["Death Certificate"])

@router.post("/register")
async def register_death(data: dict, db: Session = Depends(get_db)):
    deceased_name = data.get("deceased_name")
    citizen_id = data.get("citizen_id")
    hospital_id = data.get("hospital_id")
    date_of_death = data.get("date_of_death")
    cause_of_death = data.get("cause_of_death")

    if not deceased_name:
        raise HTTPException(status_code=400, detail="deceased_name required")

    cert_id = f"DC-{uuid.uuid4().hex[:8].upper()}"
    new_cert = DeathCertificate(
        id=cert_id,
        deceased_name=deceased_name,
        citizen_id=citizen_id,
        hospital_id=hospital_id,
        date_of_death=date_of_death,
        cause_of_death=cause_of_death,
        status="applied"
    )
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    return {"certificate_id": cert_id, "status": "applied", "message": "Death registered"}

@router.get("/status/{certificate_id}")
async def get_death_status(certificate_id: str, db: Session = Depends(get_db)):
    cert = db.query(DeathCertificate).filter(DeathCertificate.id == certificate_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return {
        "certificate_id": cert.id,
        "deceased_name": cert.deceased_name,
        "status": cert.status,
        "issued_at": cert.issued_at
    }
