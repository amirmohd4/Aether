from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.admission import Admission

router = APIRouter(prefix="/admission", tags=["Admission"])

@router.post("/apply")
async def apply_admission(data: dict, db: Session = Depends(get_db)):
    student_name = data.get("student_name")
    citizen_id = data.get("citizen_id")
    school_id = data.get("school_id")
    class_grade = data.get("class_grade")
    admission_year = data.get("admission_year")

    if not student_name or not citizen_id:
        raise HTTPException(status_code=400, detail="student_name and citizen_id required")

    app_id = f"ADM-{uuid.uuid4().hex[:8].upper()}"
    new_app = Admission(
        id=app_id,
        student_name=student_name,
        citizen_id=citizen_id,
        school_id=school_id,
        class_grade=class_grade,
        admission_year=admission_year,
        status="applied"
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return {"application_id": app_id, "status": "applied", "message": "Admission applied"}

@router.get("/status/{app_id}")
async def get_admission_status(app_id: str, db: Session = Depends(get_db)):
    app = db.query(Admission).filter(Admission.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "application_id": app.id,
        "student_name": app.student_name,
        "status": app.status,
        "enrolled_at": app.enrolled_at
    }
