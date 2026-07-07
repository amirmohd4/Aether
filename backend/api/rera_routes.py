from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.database_models import Property

router = APIRouter(prefix="/rera", tags=["RERA"])

@router.get("/verify/{property_id}")
async def rera_verify(property_id: str, db: Session = Depends(get_db)):
    """
    Verify if property has RERA registration (for under‑construction projects).
    """
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Simulate RERA verification
    rera_status = {
        "property_id": property_id,
        "rera_registered": False,
        "project_name": None,
        "rera_number": None,
        "completion_status": "not_applicable"
    }
    
    # For demo, if property_type is residential and value > 10,000,000, assume RERA registered
    if prop.property_type == "residential" and prop.property_value > 10000000:
        rera_status.update({
            "rera_registered": True,
            "project_name": f"Project-{property_id}",
            "rera_number": f"RERA-{property_id[:4]}-{property_id[4:8]}",
            "completion_status": "in_progress"
        })
    
    return rera_status
