from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.farmer_id import FarmerID

router = APIRouter(prefix="/farmer", tags=["Farmer ID"])


@router.post("/apply")
async def apply_farmer_id(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    farmer_name = data.get("farmer_name")
    father_name = data.get("father_name")
    village = data.get("village")
    tehsil = data.get("tehsil")
    district = data.get("district")
    state = data.get("state")
    land_area_acres = data.get("land_area_acres", 0.0)
    survey_number = data.get("survey_number", "")
    crop_type = data.get("crop_type", "")

    if not citizen_id or not farmer_name:
        raise HTTPException(status_code=400, detail="citizen_id and farmer_name required")

    farmer_id = f"FID-{uuid.uuid4().hex[:8].upper()}"
    new_farmer = FarmerID(
        id=farmer_id,
        citizen_id=citizen_id,
        farmer_name=farmer_name,
        father_name=father_name,
        village=village,
        tehsil=tehsil,
        district=district,
        state=state,
        land_area_acres=land_area_acres,
        survey_number=survey_number,
        crop_type=crop_type,
        status="applied",
    )
    db.add(new_farmer)
    db.commit()
    db.refresh(new_farmer)

    return {
        "farmer_id": farmer_id,
        "status": "applied",
        "message": "Farmer ID application submitted",
    }


@router.get("/status/{farmer_id}")
async def get_farmer_id_status(farmer_id: str, db: Session = Depends(get_db)):
    farmer = db.query(FarmerID).filter(FarmerID.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer ID not found")
    return {
        "farmer_id": farmer.id,
        "farmer_name": farmer.farmer_name,
        "status": farmer.status,
        "issued_at": farmer.issued_at,
    }
