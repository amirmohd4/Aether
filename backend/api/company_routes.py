from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.company_registration import CompanyRegistration

router = APIRouter(prefix="/company", tags=["Company Registration (MCA)"])


@router.post("/apply")
async def apply_company(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    company_name = data.get("company_name")
    company_type = data.get("company_type")
    authorised_capital = data.get("authorised_capital", 0.0)
    paid_up_capital = data.get("paid_up_capital", 0.0)
    directors = data.get("directors", "")
    registered_office = data.get("registered_office")
    state = data.get("state")

    if not citizen_id or not company_name:
        raise HTTPException(status_code=400, detail="citizen_id and company_name required")

    company_id = f"CORP-{uuid.uuid4().hex[:8].upper()}"
    new_company = CompanyRegistration(
        id=company_id,
        citizen_id=citizen_id,
        company_name=company_name,
        company_type=company_type,
        authorised_capital=authorised_capital,
        paid_up_capital=paid_up_capital,
        directors=directors,
        registered_office=registered_office,
        state=state,
        status="applied",
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return {
        "registration_id": company_id,
        "status": "applied",
        "message": "Company registration application submitted to MCA",
    }


@router.get("/status/{registration_id}")
async def get_company_status(registration_id: str, db: Session = Depends(get_db)):
    company = db.query(CompanyRegistration).filter(CompanyRegistration.id == registration_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Registration not found")
    return {
        "registration_id": company.id,
        "company_name": company.company_name,
        "company_type": company.company_type,
        "status": company.status,
        "cin": company.cin,
        "fee_paid": company.fee_paid,
        "issued_at": company.issued_at,
    }
