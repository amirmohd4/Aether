from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.crop_insurance import CropInsurance

router = APIRouter(prefix="/crop-insurance", tags=["Crop Insurance"])


@router.post("/apply")
async def apply_crop_insurance(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    farmer_id = data.get("farmer_id")
    farmer_name = data.get("farmer_name")
    crop_name = data.get("crop_name")
    area_acres = data.get("area_acres", 0.0)
    sum_insured = data.get("sum_insured", 0.0)
    premium_amount = data.get("premium_amount", 0.0)
    season = data.get("season", "kharif")
    village = data.get("village")
    district = data.get("district")
    state = data.get("state")

    if not citizen_id or not farmer_name or not crop_name:
        raise HTTPException(status_code=400, detail="citizen_id, farmer_name and crop_name required")

    insurance_id = f"CINS-{uuid.uuid4().hex[:8].upper()}"
    new_insurance = CropInsurance(
        id=insurance_id,
        citizen_id=citizen_id,
        farmer_id=farmer_id,
        farmer_name=farmer_name,
        crop_name=crop_name,
        area_acres=area_acres,
        sum_insured=sum_insured,
        premium_amount=premium_amount,
        season=season,
        village=village,
        district=district,
        state=state,
        status="applied",
    )
    db.add(new_insurance)
    db.commit()
    db.refresh(new_insurance)

    return {
        "insurance_id": insurance_id,
        "status": "applied",
        "message": "Crop insurance application submitted",
    }


@router.get("/status/{insurance_id}")
async def get_crop_insurance_status(insurance_id: str, db: Session = Depends(get_db)):
    insurance = db.query(CropInsurance).filter(CropInsurance.id == insurance_id).first()
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance application not found")
    return {
        "insurance_id": insurance.id,
        "farmer_name": insurance.farmer_name,
        "crop_name": insurance.crop_name,
        "status": insurance.status,
        "claim_amount": insurance.claim_amount,
        "claim_settled_at": insurance.claim_settled_at,
        "issued_at": insurance.issued_at,
    }
