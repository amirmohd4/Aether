from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.scholarship import Scholarship

router = APIRouter(prefix="/scholarship", tags=["Scholarship"])

@router.post("/apply")
async def apply_scholarship(data: dict, db: Session = Depends(get_db)):
    student_name = data.get("student_name")
    citizen_id = data.get("citizen_id")
    income = data.get("income")
    caste = data.get("caste")
    marks = data.get("marks")
    college_id = data.get("college_id")
    course = data.get("course")

    if not student_name or not citizen_id:
        raise HTTPException(status_code=400, detail="student_name and citizen_id required")

    app_id = f"SCH-{uuid.uuid4().hex[:8].upper()}"
    new_app = Scholarship(
        id=app_id,
        student_name=student_name,
        citizen_id=citizen_id,
        income=income,
        caste=caste,
        marks=marks,
        college_id=college_id,
        course=course,
        status="applied"
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return {"application_id": app_id, "status": "applied", "message": "Scholarship applied"}

@router.get("/status/{app_id}")
async def get_scholarship_status(app_id: str, db: Session = Depends(get_db)):
    app = db.query(Scholarship).filter(Scholarship.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "application_id": app.id,
        "student_name": app.student_name,
        "status": app.status,
        "amount": app.amount,
        "disbursed_at": app.disbursed_at
    }
