from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.police_clearance import PoliceClearanceCertificate

router = APIRouter(prefix="/police-clearance", tags=["Police Clearance Certificate"])


@router.post("/apply")
async def apply_police_clearance(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    applicant_name = data.get("applicant_name")
    father_name = data.get("father_name")
    address = data.get("address")
    district = data.get("district")
    state = data.get("state")
    purpose = data.get("purpose")  # employment, immigration, visa, other
    passport_number = data.get("passport_number")

    if not citizen_id or not applicant_name:
        raise HTTPException(status_code=400, detail="citizen_id and applicant_name required")

    pcc_id = f"PCC-{uuid.uuid4().hex[:8].upper()}"
    new_pcc = PoliceClearanceCertificate(
        id=pcc_id,
        citizen_id=citizen_id,
        applicant_name=applicant_name,
        father_name=father_name,
        address=address,
        district=district,
        state=state,
        purpose=purpose,
        passport_number=passport_number,
        status="applied",
    )
    db.add(new_pcc)
    db.commit()
    db.refresh(new_pcc)

    return {
        "certificate_id": pcc_id,
        "status": "applied",
        "message": "Police clearance certificate application submitted",
    }


@router.get("/status/{certificate_id}")
async def get_police_clearance_status(certificate_id: str, db: Session = Depends(get_db)):
    pcc = db.query(PoliceClearanceCertificate).filter(PoliceClearanceCertificate.id == certificate_id).first()
    if not pcc:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return {
        "certificate_id": pcc.id,
        "applicant_name": pcc.applicant_name,
        "status": pcc.status,
        "fee_paid": pcc.fee_paid,
        "issued_at": pcc.issued_at,
        "expires_at": pcc.expires_at,
    }
