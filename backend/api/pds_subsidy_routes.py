from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.pds_subsidy import PDSSubsidy

router = APIRouter(prefix="/pds-subsidy", tags=["PDS Subsidy"])


@router.post("/apply")
async def apply_pds_subsidy(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    ration_card_id = data.get("ration_card_id")
    beneficiary_name = data.get("beneficiary_name")
    subsidy_type = data.get("subsidy_type")  # food, lpg, fertilizer
    amount = data.get("amount", 0.0)
    bank_account = data.get("bank_account")
    ifsc_code = data.get("ifsc_code")

    if not citizen_id or not ration_card_id:
        raise HTTPException(status_code=400, detail="citizen_id and ration_card_id required")

    subsidy_id = f"PDS-{uuid.uuid4().hex[:8].upper()}"
    new_subsidy = PDSSubsidy(
        id=subsidy_id,
        citizen_id=citizen_id,
        ration_card_id=ration_card_id,
        beneficiary_name=beneficiary_name,
        subsidy_type=subsidy_type,
        amount=amount,
        bank_account=bank_account,
        ifsc_code=ifsc_code,
        status="applied",
    )
    db.add(new_subsidy)
    db.commit()
    db.refresh(new_subsidy)

    return {
        "subsidy_id": subsidy_id,
        "status": "applied",
        "message": f"PDS subsidy ({subsidy_type}) application submitted",
    }


@router.get("/status/{subsidy_id}")
async def get_pds_subsidy_status(subsidy_id: str, db: Session = Depends(get_db)):
    subsidy = db.query(PDSSubsidy).filter(PDSSubsidy.id == subsidy_id).first()
    if not subsidy:
        raise HTTPException(status_code=404, detail="Subsidy application not found")
    return {
        "subsidy_id": subsidy.id,
        "beneficiary_name": subsidy.beneficiary_name,
        "subsidy_type": subsidy.subsidy_type,
        "amount": subsidy.amount,
        "status": subsidy.status,
        "disbursed_at": subsidy.disbursed_at,
    }
