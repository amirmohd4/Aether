from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.gst_registration import GSTRegistration

router = APIRouter(prefix="/gst", tags=["GST Registration"])


@router.post("/apply")
async def apply_gst(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    business_name = data.get("business_name")
    business_type = data.get("business_type")
    pan_number = data.get("pan_number")
    aadhaar_number = data.get("aadhaar_number")
    address = data.get("address")
    district = data.get("district")
    state = data.get("state")
    turnover = data.get("turnover", 0.0)

    if not citizen_id or not business_name or not pan_number:
        raise HTTPException(status_code=400, detail="citizen_id, business_name and pan_number required")

    gst_id = f"GST-{uuid.uuid4().hex[:8].upper()}"
    new_reg = GSTRegistration(
        id=gst_id,
        citizen_id=citizen_id,
        business_name=business_name,
        business_type=business_type,
        pan_number=pan_number,
        aadhaar_number=aadhaar_number,
        address=address,
        district=district,
        state=state,
        turnover=turnover,
        status="applied",
    )
    db.add(new_reg)
    db.commit()
    db.refresh(new_reg)

    return {
        "registration_id": gst_id,
        "status": "applied",
        "message": "GST registration application submitted",
    }


@router.get("/status/{registration_id}")
async def get_gst_status(registration_id: str, db: Session = Depends(get_db)):
    reg = db.query(GSTRegistration).filter(GSTRegistration.id == registration_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")
    return {
        "registration_id": reg.id,
        "business_name": reg.business_name,
        "status": reg.status,
        "gstin": reg.gstin,
        "fee_paid": reg.fee_paid,
        "issued_at": reg.issued_at,
    }
