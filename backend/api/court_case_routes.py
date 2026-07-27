from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.court_case_filing import CourtCaseFiling

router = APIRouter(prefix="/court-case", tags=["Court Case Filing"])


@router.post("/apply")
async def file_court_case(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    petitioner_name = data.get("petitioner_name")
    respondent_name = data.get("respondent_name")
    case_type = data.get("case_type")
    court_name = data.get("court_name")
    district = data.get("district")
    state = data.get("state")
    subject = data.get("subject")
    description = data.get("description", "")
    documents = data.get("documents", [])

    if not citizen_id or not petitioner_name:
        raise HTTPException(status_code=400, detail="citizen_id and petitioner_name required")

    case_id = f"CCF-{uuid.uuid4().hex[:8].upper()}"
    new_case = CourtCaseFiling(
        id=case_id,
        citizen_id=citizen_id,
        petitioner_name=petitioner_name,
        respondent_name=respondent_name,
        case_type=case_type,
        court_name=court_name,
        district=district,
        state=state,
        subject=subject,
        description=description,
        documents=documents,
        status="filed",
        filed_at=datetime.utcnow(),
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return {
        "case_id": case_id,
        "status": "filed",
        "message": "Court case filed successfully",
    }


@router.get("/status/{case_id}")
async def get_court_case_status(case_id: str, db: Session = Depends(get_db)):
    case = db.query(CourtCaseFiling).filter(CourtCaseFiling.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return {
        "case_id": case.id,
        "petitioner_name": case.petitioner_name,
        "respondent_name": case.respondent_name,
        "case_type": case.case_type,
        "status": case.status,
        "case_number": case.case_number,
        "next_hearing": case.next_hearing,
        "filed_at": case.filed_at,
    }
