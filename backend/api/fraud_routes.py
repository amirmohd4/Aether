from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from backend.database import get_db  # <-- FIXED
from backend.services.fraud_service import fraud_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/detect")
async def detect_fraud(property_data: Dict[str, Any]):
    """Detect fraud in property data"""
    try:
        result = fraud_service.detect_fraud(property_data)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Fraud detection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{property_id}")
async def get_fraud_status(property_id: str):
    """Get fraud status for a property"""
    # Mock response for now
    return {
        "property_id": property_id,
        "status": "clean",
        "score": 0.1,
        "checks": ["title_verified", "no_encumbrance"]
    }
