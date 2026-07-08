from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.trade_license import TradeLicense

router = APIRouter(prefix="/trade-license", tags=["Trade License"])

@router.post("/apply")
async def apply_trade_license(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    business_name = data.get("business_name")
    business_type = data.get("business_type")
    address = data.get("address")

    if not citizen_id or not business_name:
        raise HTTPException(status_code=400, detail="citizen_id and business_name required")

    license_id = f"TL-{uuid.uuid4().hex[:8].upper()}"

    new_license = TradeLicense(
        id=license_id,
        citizen_id=citizen_id,
        business_name=business_name,
        business_type=business_type,
        address=address,
        status="applied",
        nocs={"fire": "pending", "health": "pending", "pollution": "pending", "water": "pending"}
    )
    db.add(new_license)
    db.commit()
    db.refresh(new_license)

    return {
        "license_id": license_id,
        "status": "applied",
        "nocs": new_license.nocs,
        "message": "Trade license application submitted. NOCs requested."
    }

@router.get("/status/{license_id}")
async def get_trade_license_status(license_id: str, db: Session = Depends(get_db)):
    license = db.query(TradeLicense).filter(TradeLicense.id == license_id).first()
    if not license:
        raise HTTPException(status_code=404, detail="License not found")
    return {
        "license_id": license.id,
        "status": license.status,
        "nocs": license.nocs,
        "fee_paid": license.fee_paid,
        "issued_at": license.issued_at,
        "expires_at": license.expires_at
    }
