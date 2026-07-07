from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.database_models import Property

router = APIRouter(prefix="/cersai", tags=["CERSAI"])

@router.get("/check/{property_id}")
async def cersai_check(property_id: str, db: Session = Depends(get_db)):
    """
    Check if property has any existing loan registered with CERSAI.
    """
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Simulate CERSAI check
    existing_loans = []
    # Randomly simulate loans based on encumbrance data
    if prop.encumbrances:
        for enc in prop.encumbrances:
            if enc.get("type") == "mortgage":
                existing_loans.append({
                    "loan_id": f"LOAN-{enc.get('amount', 0):.0f}",
                    "amount": enc.get("amount", 0),
                    "creditor": enc.get("creditor", "Unknown")
                })
    
    return {
        "property_id": property_id,
        "has_loan": len(existing_loans) > 0,
        "loans": existing_loans,
        "source": "CERSAI"
    }
