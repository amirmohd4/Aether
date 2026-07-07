from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.database_models import Property
from typing import List

router = APIRouter(prefix="/public", tags=["Public"])

@router.get("/search/{property_id}")
async def public_search(property_id: str, db: Session = Depends(get_db)):
    """
    Public search without login – returns limited property details.
    """
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Return only non-sensitive fields
    return {
        "property_id": prop.property_id,
        "district": prop.district,
        "village": prop.village,
        "owner": prop.owner,  # Might be sensitive, but for demo we include
        "property_type": prop.property_type,
        "property_size": prop.property_size,
        "property_value": prop.property_value,
        "title_status": prop.title_status
    }

@router.get("/search/by-district/{district}")
async def public_search_district(district: str, limit: int = 10, db: Session = Depends(get_db)):
    properties = db.query(Property).filter(Property.district.ilike(f"%{district}%")).limit(limit).all()
    return [
        {
            "property_id": p.property_id,
            "owner": p.owner,
            "district": p.district,
            "property_value": p.property_value
        }
        for p in properties
    ]
