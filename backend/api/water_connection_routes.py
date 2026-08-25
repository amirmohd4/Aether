from fastapi import APIRouter, HTTPException, Depends  # <-- FIXED: APIRouter (no space)
from sqlalchemy.orm import Session
import uuid
from backend.database import get_db  # <-- FIXED: use backend.database
from backend.models.water_connection import WaterConnection  # <-- FIXED: use backend.models

router = APIRouter(prefix="/water-connection", tags=["Water Connection"])

@router.post("/apply")
async def apply_water_connection(data: dict, db: Session = Depends(get_db)):
    property_id = data.get("property_id")
    citizen_id = data.get("citizen_id")
    connection_type = data.get("connection_type", "residential")

    if not property_id or not citizen_id:
        raise HTTPException(status_code=400, detail="Property_id and citizen_id required")
    
    # Generate application ID
    application_id = f"WC-{uuid.uuid4().hex[:8].upper()}"
    
    return {
        "status": "success",
        "application_id": application_id,
        "property_id": property_id,
        "citizen_id": citizen_id,
        "connection_type": connection_type,
        "message": "Water connection application submitted successfully"
    }
