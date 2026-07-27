from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.rera_certificate import RERACertificate

router = APIRouter(prefix="/rera-certificate", tags=["RERA Certificate"])


@router.post("/apply")
async def apply_rera_certificate(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    project_name = data.get("project_name")
    developer_name = data.get("developer_name")
    project_id = data.get("project_id")
    certificate_type = data.get("certificate_type", "registration")

    if not citizen_id or not project_name:
        raise HTTPException(status_code=400, detail="citizen_id and project_name required")

    cert_id = f"RERA-C-{uuid.uuid4().hex[:8].upper()}"
    new_cert = RERACertificate(
        id=cert_id,
        citizen_id=citizen_id,
        project_name=project_name,
        developer_name=developer_name,
        project_id=project_id,
        certificate_type=certificate_type,
        status="applied",
    )
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)

    return {
        "certificate_id": cert_id,
        "status": "applied",
        "message": "RERA certificate application submitted",
    }


@router.get("/status/{certificate_id}")
async def get_rera_certificate_status(certificate_id: str, db: Session = Depends(get_db)):
    cert = db.query(RERACertificate).filter(RERACertificate.id == certificate_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return {
        "certificate_id": cert.id,
        "project_name": cert.project_name,
        "developer_name": cert.developer_name,
        "status": cert.status,
        "rera_number": cert.rera_number,
        "fee_paid": cert.fee_paid,
        "issued_at": cert.issued_at,
        "expires_at": cert.expires_at,
    }
