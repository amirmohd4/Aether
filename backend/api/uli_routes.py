from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.database_models import Property

router = APIRouter(prefix="/uli", tags=["ULI"])

@router.get("/verify/{property_id}")
async def uli_verify(property_id: str, db: Session = Depends(get_db)):
    """
    Simulate RBI ULI (Unified Lending Interface) integration.
    Returns land record status from official ULI channel.
    """
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Simulate ULI response (official land records)
    return {
        "uli_status": "verified",
        "source": "ULI",
        "property_id": prop.property_id,
        "owner": prop.owner,
        "title_status": prop.title_status,
        "encumbrances": prop.encumbrances or [],
        "timestamp": "2026-07-07T12:00:00Z"
    }
