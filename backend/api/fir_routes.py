from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.fir_report import FIRReport

router = APIRouter(prefix="/fir", tags=["FIR Report"])


@router.post("/apply")
async def file_fir(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    complainant_name = data.get("complainant_name")
    accused_name = data.get("accused_name")
    incident_date = data.get("incident_date")
    incident_location = data.get("incident_location")
    police_station = data.get("police_station")
    district = data.get("district")
    state = data.get("state")
    fir_sections = data.get("fir_sections", "")
    description = data.get("description", "")

    if not citizen_id or not complainant_name:
        raise HTTPException(status_code=400, detail="citizen_id and complainant_name required")

    fir_id = f"FIR-{uuid.uuid4().hex[:8].upper()}"
    parsed_date = None
    if incident_date:
        try:
            parsed_date = datetime.fromisoformat(incident_date.replace("Z", ""))
        except Exception:
            parsed_date = datetime.utcnow()

    new_fir = FIRReport(
        id=fir_id,
        citizen_id=citizen_id,
        complainant_name=complainant_name,
        accused_name=accused_name,
        incident_date=parsed_date,
        incident_location=incident_location,
        police_station=police_station,
        district=district,
        state=state,
        fir_sections=fir_sections,
        description=description,
        status="filed",
        filed_at=datetime.utcnow(),
    )
    db.add(new_fir)
    db.commit()
    db.refresh(new_fir)

    return {
        "fir_id": fir_id,
        "status": "filed",
        "message": "FIR report filed successfully",
    }


@router.get("/status/{fir_id}")
async def get_fir_status(fir_id: str, db: Session = Depends(get_db)):
    fir = db.query(FIRReport).filter(FIRReport.id == fir_id).first()
    if not fir:
        raise HTTPException(status_code=404, detail="FIR not found")
    return {
        "fir_id": fir.id,
        "complainant_name": fir.complainant_name,
        "status": fir.status,
        "police_station": fir.police_station,
        "filed_at": fir.filed_at,
    }
