from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.schemas import FraudAlertResponse
from models.database_models import FraudDetectionLog
from services import fraud_service

router = APIRouter(prefix="/fraud", tags=["Fraud Detection"])

@router.post("/detect/{property_id}")
async def detect_fraud(
    property_id: str,
    workflow_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Run fraud detection on a property
    Returns fraud score (0-100) with explanation
    """
    try:
        result = fraud_service.detect_fraud(db, property_id, workflow_id)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alert/{fraud_id}")
async def get_fraud_alert(fraud_id: str, db: Session = Depends(get_db)):
    """
    Get fraud alert details with explanation
    """
    try:
        fraud_log = fraud_service.get_fraud_alert(db, fraud_id)
        
        # Color coding based on severity
        color_map = {
            "low": "#4CAF50",      # Green
            "medium": "#FF9800",   # Orange
            "high": "#F44336",     # Red
            "critical": "#B71C1C"  # Dark Red
        }
        
        return {
            "fraud_id": fraud_log.fraud_id,
            "property_id": fraud_log.property_id,
            "workflow_id": fraud_log.workflow_id,
            "fraud_type": fraud_log.fraud_type,
            "severity": fraud_log.severity.value,
            "severity_color": color_map.get(fraud_log.severity.value, "#757575"),
            "fraud_score": fraud_log.fraud_score,
            "description": fraud_log.description,
            "explanation": fraud_log.explanation,
            "evidence": fraud_log.evidence,
            "flagged_at": fraud_log.flagged_at.isoformat(),
            "resolved": fraud_log.resolved,
            "resolution_notes": fraud_log.resolution_notes
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alert/{fraud_id}/resolve")
async def resolve_fraud_alert(
    fraud_id: str,
    resolution_notes: str,
    db: Session = Depends(get_db)
):
    """
    Mark fraud alert as resolved
    """
    try:
        fraud_service.resolve_fraud_alert(db, fraud_id, resolution_notes)
        
        return {
            "fraud_id": fraud_id,
            "status": "resolved",
            "resolution_notes": resolution_notes,
            "message": "Fraud alert resolved successfully"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/by-property/{property_id}")
async def get_fraud_alerts_by_property(
    property_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all fraud alerts for a property
    """
    try:
        fraud_logs = db.query(FraudDetectionLog).filter(
            FraudDetectionLog.property_id == property_id
        ).order_by(FraudDetectionLog.flagged_at.desc()).all()
        
        result = []
        for log in fraud_logs:
            result.append({
                "fraud_id": log.fraud_id,
                "fraud_type": log.fraud_type,
                "severity": log.severity.value,
                "fraud_score": log.fraud_score,
                "description": log.description,
                "flagged_at": log.flagged_at.isoformat(),
                "resolved": log.resolved
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/high-risk")
async def get_high_risk_alerts(db: Session = Depends(get_db)):
    """
    Get all high-risk and critical fraud alerts
    """
    try:
        from models.database_models import FraudSeverityEnum
        
        fraud_logs = db.query(FraudDetectionLog).filter(
            FraudDetectionLog.severity.in_([
                FraudSeverityEnum.high,
                FraudSeverityEnum.critical
            ]),
            FraudDetectionLog.resolved == False
        ).order_by(FraudDetectionLog.fraud_score.desc()).limit(50).all()
        
        result = []
        for log in fraud_logs:
            result.append({
                "fraud_id": log.fraud_id,
                "property_id": log.property_id,
                "workflow_id": log.workflow_id,
                "fraud_type": log.fraud_type,
                "severity": log.severity.value,
                "fraud_score": log.fraud_score,
                "description": log.description,
                "explanation": log.explanation,
                "flagged_at": log.flagged_at.isoformat()
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train-model")
async def train_fraud_model(db: Session = Depends(get_db)):
    """
    Train/retrain the fraud detection AI model
    """
    try:
        fraud_service.train_model(db)
        
        return {
            "status": "success",
            "message": "Fraud detection model trained successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
