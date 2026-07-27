from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models.factory_license import FactoryLicense

router = APIRouter(prefix="/factory-license", tags=["Factory License"])


@router.post("/apply")
async def apply_factory_license(data: dict, db: Session = Depends(get_db)):
    citizen_id = data.get("citizen_id")
    factory_name = data.get("factory_name")
    factory_type = data.get("factory_type")
    address = data.get("address")
    district = data.get("district")
    state = data.get("state")
    employee_count = data.get("employee_count", 0)
    machinery_details = data.get("machinery_details", "")

    if not citizen_id or not factory_name:
        raise HTTPException(status_code=400, detail="citizen_id and factory_name required")

    license_id = f"FL-{uuid.uuid4().hex[:8].upper()}"
    new_license = FactoryLicense(
        id=license_id,
        citizen_id=citizen_id,
        factory_name=factory_name,
        factory_type=factory_type,
        address=address,
        district=district,
        state=state,
        employee_count=employee_count,
        machinery_details=machinery_details,
        status="applied",
        nocs={"factory": "pending", "boiler": "pending", "labour": "pending"},
    )
    db.add(new_license)
    db.commit()
    db.refresh(new_license)

    return {
        "license_id": license_id,
        "status": "applied",
        "nocs": new_license.nocs,
        "message": "Factory license application submitted. NOCs requested.",
    }


@router.get("/status/{license_id}")
async def get_factory_license_status(license_id: str, db: Session = Depends(get_db)):
    license = db.query(FactoryLicense).filter(FactoryLicense.id == license_id).first()
    if not license:
        raise HTTPException(status_code=404, detail="License not found")
    return {
        "license_id": license.id,
        "factory_name": license.factory_name,
        "status": license.status,
        "nocs": license.nocs,
        "fee_paid": license.fee_paid,
        "issued_at": license.issued_at,
        "expires_at": license.expires_at,
    }
