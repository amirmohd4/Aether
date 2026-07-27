from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.e_court import ECourt

router = APIRouter(prefix="/e-court", tags=["E-Court"])


@router.post("/apply")
async def create_e_court(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    case_number = data.get("case_number")
    court_name = data.get("court_name")
    petitioner = data.get("petitioner")
    respondent = data.get("respondent")
    hearing_date = data.get("hearing_date")
    notes = data.get("notes", "")
    documents = data.get("documents", [])

    if not citizen_id or not case_number:
        raise HTTPException(status_code=400, detail="citizen_id and case_number required")

    e_court_id = f"EC-{uuid.uuid4().hex[:8].upper()}"
    parsed_hearing = None
    if hearing_date:
        try:
            parsed_hearing = datetime.fromisoformat(hearing_date.replace("Z", ""))
        except Exception:
            parsed_hearing = None

    new_e_court = ECourt(
        id=e_court_id,
        citizen_id=citizen_id,
        case_number=case_number,
        court_name=court_name,
        petitioner=petitioner,
        respondent=respondent,
        hearing_date=parsed_hearing,
        status="scheduled",
        documents=documents,
        notes=notes,
    )
    db.add(new_e_court)
    db.commit()
    db.refresh(new_e_court)

    return {
        "e_court_id": e_court_id,
        "status": "scheduled",
        "message": "E-Court hearing scheduled",
    }


@router.get("/status/{e_court_id}")
async def get_e_court_status(e_court_id: str, db: Session = Depends(get_db)):
    e_court = db.query(ECourt).filter(ECourt.id == e_court_id).first()
    if not e_court:
        raise HTTPException(status_code=404, detail="E-Court record not found")
    return {
        "e_court_id": e_court.id,
        "case_number": e_court.case_number,
        "court_name": e_court.court_name,
        "petitioner": e_court.petitioner,
        "respondent": e_court.respondent,
        "status": e_court.status,
        "hearing_date": e_court.hearing_date,
    }
