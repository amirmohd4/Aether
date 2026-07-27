from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.ration_card import RationCard

router = APIRouter(prefix="/ration-card", tags=["Ration Card"])


@router.post("/apply")
async def apply_ration_card(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    head_of_family = data.get("head_of_family")
    card_type = data.get("card_type")  # AAY, BPL, APL
    address = data.get("address")
    district = data.get("district")
    state = data.get("state")
    members = data.get("members", [])
    annual_income = data.get("annual_income", 0.0)

    if not citizen_id or not head_of_family:
        raise HTTPException(status_code=400, detail="citizen_id and head_of_family required")

    card_id = f"RC-{uuid.uuid4().hex[:8].upper()}"
    new_card = RationCard(
        id=card_id,
        citizen_id=citizen_id,
        head_of_family=head_of_family,
        card_type=card_type,
        address=address,
        district=district,
        state=state,
        members=members,
        annual_income=annual_income,
        status="applied",
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)

    return {
        "card_id": card_id,
        "status": "applied",
        "message": "Ration card application submitted",
    }


@router.get("/status/{card_id}")
async def get_ration_card_status(card_id: str, db: Session = Depends(get_db)):
    card = db.query(RationCard).filter(RationCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Ration card not found")
    return {
        "card_id": card.id,
        "head_of_family": card.head_of_family,
        "card_type": card.card_type,
        "status": card.status,
        "issued_at": card.issued_at,
        "expires_at": card.expires_at,
    }
