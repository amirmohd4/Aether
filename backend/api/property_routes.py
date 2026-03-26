from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.schemas import PropertyResponse
from models.database_models import Property
from services import connector_service, cache
from typing import List

router = APIRouter(prefix="/property", tags=["Property"])

@router.get("/{property_id}", response_model=dict)
async def get_property(property_id: str, db: Session = Depends(get_db)):
    """
    Get unified property data from all connectors
    Uses cache-first strategy
    """
    try:
        # Check database first
        db_property = db.query(Property).filter(Property.property_id == property_id).first()
        
        if not db_property:
            raise HTTPException(status_code=404, detail=f"Property {property_id} not found")
        
        # Get unified connector data
        connector_data = connector_service.fetch_property_unified(property_id)
        
        # Combine database property with connector data
        response = {
            "property_id": db_property.property_id,
            "state": db_property.state,
            "location": db_property.location,
            "district": db_property.district,
            "tehsil": db_property.tehsil,
            "village": db_property.village,
            "owner": db_property.owner,
            "title_status": db_property.title_status,
            "property_value": db_property.property_value,
            "property_size": db_property.property_size,
            "property_type": db_property.property_type,
            "encumbrances": db_property.encumbrances,
            "history": db_property.history,
            "state_specific_data": db_property.state_specific_data,
            "created_at": db_property.created_at.isoformat(),
            "updated_at": db_property.updated_at.isoformat(),
            "connector_data": connector_data
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/by-state/{state}", response_model=List[dict])
async def search_properties_by_state(
    state: str,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Search properties by state"""
    try:
        properties = db.query(Property).filter(
            Property.state == state
        ).offset(offset).limit(limit).all()
        
        result = []
        for prop in properties:
            result.append({
                "property_id": prop.property_id,
                "state": prop.state,
                "location": prop.location,
                "district": prop.district,
                "owner": prop.owner,
                "title_status": prop.title_status,
                "property_value": prop.property_value,
                "property_size": prop.property_size,
                "property_type": prop.property_type
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/by-district/{district}", response_model=List[dict])
async def search_properties_by_district(
    district: str,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Search properties by district"""
    try:
        properties = db.query(Property).filter(
            Property.district.ilike(f"%{district}%")
        ).offset(offset).limit(limit).all()
        
        result = []
        for prop in properties:
            result.append({
                "property_id": prop.property_id,
                "state": prop.state,
                "location": prop.location,
                "district": prop.district,
                "owner": prop.owner,
                "title_status": prop.title_status,
                "property_value": prop.property_value,
                "property_size": prop.property_size,
                "property_type": prop.property_type
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify-title/{property_id}")
async def verify_property_title(property_id: str, db: Session = Depends(get_db)):
    """Verify property title across all relevant connectors"""
    try:
        # Check if property exists
        db_property = db.query(Property).filter(Property.property_id == property_id).first()
        if not db_property:
            raise HTTPException(status_code=404, detail=f"Property {property_id} not found")
        
        result = connector_service.verify_title(property_id)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-encumbrance/{property_id}")
async def check_property_encumbrance(property_id: str, db: Session = Depends(get_db)):
    """Check property encumbrances across all relevant connectors"""
    try:
        # Check if property exists
        db_property = db.query(Property).filter(Property.property_id == property_id).first()
        if not db_property:
            raise HTTPException(status_code=404, detail=f"Property {property_id} not found")
        
        result = connector_service.check_encumbrance(property_id)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
