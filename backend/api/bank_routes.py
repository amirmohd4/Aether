from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from database import SessionLocal
from models.database_models import Property, WorkflowState

router = APIRouter(prefix="/bank", tags=["Bank"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/verify-title")
async def verify_title(
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Bank API: Instant title verification with encumbrance, fraud score, valuation.
    """
    property_id = data.get("property_id")
    bank_id = data.get("bank_id", "BANK-DEMO")
    
    if not property_id:
        raise HTTPException(status_code=400, detail="property_id required")
    
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Get encumbrance from property history or separate table
    encumbrance = prop.encumbrances or []
    
    # Compute fraud score (simulate from fraud detection model)
    fraud_score = 9.0  # placeholder, use real fraud detection if available
    severity = "LOW"
    
    # Simple valuation (could be AI-based)
    valuation = prop.property_value
    
    return {
        "property_id": prop.property_id,
        "title_clear": prop.title_status == "clear",
        "title_status": prop.title_status,
        "encumbrance": encumbrance,
        "fraud_score": fraud_score,
        "severity": severity,
        "valuation": valuation,
        "bank_id": bank_id
    }

@router.get("/encumbrance/{property_id}")
async def get_encumbrance(
    property_id: str,
    db: Session = Depends(get_db)
):
    """Return encumbrance certificate for a property."""
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return {
        "property_id": prop.property_id,
        "encumbrances": prop.encumbrances or [],
        "title_status": prop.title_status
    }
