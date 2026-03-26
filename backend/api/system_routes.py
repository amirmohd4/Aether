from fastapi import APIRouter, Depends, HTTPException
from services import connector_service, cache
from sqlalchemy.orm import Session
from database import get_db
from models.database_models import Property, WorkflowState, FraudDetectionLog

router = APIRouter(prefix="/system", tags=["System"])

@router.get("/health")
async def health_check():
    """
    System health check
    """
    try:
        # Check connector health
        connector_health = connector_service.health_check()
        
        # Check cache health
        cache_health = cache.health_check()
        
        return {
            "status": "healthy",
            "connectors": connector_health,
            "cache": cache_health,
            "message": "Aether GovOS is operational"
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.get("/state-info")
async def get_state_info():
    """
    Get active state configuration
    """
    try:
        state_info = connector_service.get_state_info()
        return state_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_system_stats(db: Session = Depends(get_db)):
    """
    Get system statistics
    """
    try:
        # Count properties
        total_properties = db.query(Property).count()
        karnataka_properties = db.query(Property).filter(Property.state == "karnataka").count()
        jk_properties = db.query(Property).filter(Property.state == "jk").count()
        
        # Count workflows
        total_workflows = db.query(WorkflowState).count()
        active_workflows = db.query(WorkflowState).filter(
            WorkflowState.status.in_(["in_progress", "manual_review"])
        ).count()
        completed_workflows = db.query(WorkflowState).filter(
            WorkflowState.status == "completed"
        ).count()
        
        # Count fraud alerts
        total_fraud_alerts = db.query(FraudDetectionLog).count()
        unresolved_alerts = db.query(FraudDetectionLog).filter(
            FraudDetectionLog.resolved == False
        ).count()
        high_risk_alerts = db.query(FraudDetectionLog).filter(
            FraudDetectionLog.severity.in_(["high", "critical"]),
            FraudDetectionLog.resolved == False
        ).count()
        
        return {
            "properties": {
                "total": total_properties,
                "karnataka": karnataka_properties,
                "jk": jk_properties
            },
            "workflows": {
                "total": total_workflows,
                "active": active_workflows,
                "completed": completed_workflows
            },
            "fraud_alerts": {
                "total": total_fraud_alerts,
                "unresolved": unresolved_alerts,
                "high_risk": high_risk_alerts
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api-marketplace")
async def get_api_marketplace():
    """
    Get available APIs with mock pricing
    """
    apis = [
        {
            "api_name": "Property Data API",
            "endpoint": "/api/property/{property_id}",
            "description": "Get unified property data from all government systems",
            "method": "GET",
            "pricing": "₹2 per request",
            "rate_limit": "100 requests/minute"
        },
        {
            "api_name": "Title Verification API",
            "endpoint": "/api/property/verify-title/{property_id}",
            "description": "Verify property title across multiple systems",
            "method": "POST",
            "pricing": "₹5 per request",
            "rate_limit": "50 requests/minute"
        },
        {
            "api_name": "Encumbrance Check API",
            "endpoint": "/api/property/check-encumbrance/{property_id}",
            "description": "Check property encumbrances from all sources",
            "method": "POST",
            "pricing": "₹3 per request",
            "rate_limit": "50 requests/minute"
        },
        {
            "api_name": "Workflow API",
            "endpoint": "/api/workflow/start",
            "description": "Start property registration workflow",
            "method": "POST",
            "pricing": "₹10 per workflow",
            "rate_limit": "20 workflows/minute"
        },
        {
            "api_name": "Workflow Status API",
            "endpoint": "/api/workflow/{workflow_id}",
            "description": "Get workflow status and progress",
            "method": "GET",
            "pricing": "₹1 per request",
            "rate_limit": "100 requests/minute"
        },
        {
            "api_name": "Fraud Detection API",
            "endpoint": "/api/fraud/detect/{property_id}",
            "description": "AI-powered fraud detection with explainability",
            "method": "POST",
            "pricing": "₹15 per scan",
            "rate_limit": "30 requests/minute"
        },
        {
            "api_name": "Fraud Alert API",
            "endpoint": "/api/fraud/alert/{fraud_id}",
            "description": "Get detailed fraud alert information",
            "method": "GET",
            "pricing": "₹1 per request",
            "rate_limit": "100 requests/minute"
        },
        {
            "api_name": "Certificate API",
            "endpoint": "/api/certificate/{certificate_id}",
            "description": "Get certificate details",
            "method": "GET",
            "pricing": "₹2 per request",
            "rate_limit": "100 requests/minute"
        },
        {
            "api_name": "Property Search API",
            "endpoint": "/api/property/search/by-state/{state}",
            "description": "Search properties by state or district",
            "method": "GET",
            "pricing": "₹3 per request",
            "rate_limit": "50 requests/minute"
        },
        {
            "api_name": "State Configuration API",
            "endpoint": "/api/system/state-info",
            "description": "Get state configuration and rules",
            "method": "GET",
            "pricing": "Free",
            "rate_limit": "1000 requests/minute"
        }
    ]
    
    return {
        "marketplace": apis,
        "total_apis": len(apis),
        "authentication": "API Key required",
        "documentation": "https://docs.aether-govos.in/api"
    }


@router.get("/connectors/status")
async def get_connectors_status():
    """
    Get status of all connectors
    """
    try:
        health = connector_service.health_check()
        return health
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cache/clear")
async def clear_cache(pattern: str = "*"):
    """
    Clear cache (pattern-based)
    Admin endpoint
    """
    try:
        cache.clear_pattern(pattern)
        return {
            "status": "success",
            "message": f"Cache cleared for pattern: {pattern}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
