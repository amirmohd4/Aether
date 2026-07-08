from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.water_connection import WaterConnection

router = APIRouter(prefix="/water-connection", tags=["Water Connection"])

@router.post("/apply")
async def apply_water_connection(data: dict, db: Session = Depends(get_db)):
    property_id = data.get("property_id")
    citizen_id = data.get("citizen_id")
    connection_type = data.get("connection_type", "residential")

    if not property_id or not citizen_id:
        raise HTTPException(status_code=400, detail="property_id and citizen_id required")

    connection_id = f"WC-{uuid.uuid4().hex[:8].upper()}"

    new_connection = WaterConnection(
        id=connection_id,
        property_id=property_id,
        citizen_id=citizen_id,
        connection_type=connection_type,
        status="applied",
        fee_paid=False
    )
    db.add(new_connection)
    db.commit()
    db.refresh(new_connection)

    return {
        "connection_id": connection_id,
        "status": "applied",
        "message": "Water connection application submitted."
    }

@router.get("/status/{connection_id}")
async def get_water_connection_status(connection_id: str, db: Session = Depends(get_db)):
    conn = db.query(WaterConnection).filter(WaterConnection.id == connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")
    return {
        "connection_id": conn.id,
        "status": conn.status,
        "fee_paid": conn.fee_paid,
        "connected_at": conn.connected_at
    }
