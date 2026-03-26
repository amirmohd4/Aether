from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.database_models import Certificate
from typing import List

router = APIRouter(prefix="/certificate", tags=["Certificate"])

@router.get("/{certificate_id}")
async def get_certificate(certificate_id: str, db: Session = Depends(get_db)):
    """
    Get certificate details
    """
    try:
        certificate = db.query(Certificate).filter(
            Certificate.certificate_id == certificate_id
        ).first()
        
        if not certificate:
            raise HTTPException(status_code=404, detail=f"Certificate {certificate_id} not found")
        
        return {
            "certificate_id": certificate.certificate_id,
            "certificate_type": certificate.certificate_type,
            "citizen_id": certificate.citizen_id,
            "issuing_authority": certificate.issuing_authority,
            "status": certificate.status,
            "issue_date": certificate.issue_date.isoformat() if certificate.issue_date else None,
            "expiry_date": certificate.expiry_date.isoformat() if certificate.expiry_date else None,
            "state": certificate.state,
            "certificate_data": certificate.certificate_data,
            "created_at": certificate.created_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-citizen/{citizen_id}")
async def get_certificates_by_citizen(
    citizen_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all certificates for a citizen
    """
    try:
        certificates = db.query(Certificate).filter(
            Certificate.citizen_id == citizen_id
        ).all()
        
        result = []
        for cert in certificates:
            result.append({
                "certificate_id": cert.certificate_id,
                "certificate_type": cert.certificate_type,
                "issuing_authority": cert.issuing_authority,
                "status": cert.status,
                "issue_date": cert.issue_date.isoformat() if cert.issue_date else None,
                "state": cert.state
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
