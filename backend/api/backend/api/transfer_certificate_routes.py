from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.transfer_certificate import TransferCertificate

router = APIRouter(prefix="/transfer-certificate", tags=["Transfer Certificate"])

@router.post("/apply")
async def apply_transfer_certificate(data: dict, db: Session = Depends(get_db)):
    student_name = data.get("student_name")
    citizen_id = data.get("citizen_id")
    from_school = data.get("from_school")
    to_school = data.get("to_school")
    reason = data.get("reason")

    if not student_name or not citizen_id:
        raise HTTPException(status_code=400, detail="student_name and citizen_id required")

    app_id = f"TC-{uuid.uuid4().hex[:8].upper()}"
    new_app = TransferCertificate(
        id=app_id,
        student_name=student_name,
        citizen_id=citizen_id,
        from_school=from_school,
        to_school=to_school,
        reason=reason,
        status="applied"
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return {"application_id": app_id, "status": "applied", "message": "Transfer certificate applied"}

@router.get("/status/{app_id}")
async def get_transfer_certificate_status(app_id: str, db: Session = Depends(get_db)):
    app = db.query(TransferCertificate).filter(TransferCertificate.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "application_id": app.id,
        "student_name": app.student_name,
        "status": app.status,
        "issued_at": app.issued_at
    }
