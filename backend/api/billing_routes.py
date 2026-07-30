from fastapi import APIRouter, HTTPException, Query
from backend.services.billing_service import billing_service

router = APIRouter(prefix="/api/v1/developer/billing", tags=["Developer Billing & Metering"])

@router.get("/pricing")
def get_pricing_tiers():
    """Get public pricing tiers for developer and private sector API access."""
    return {
        "status": "success",
        "currency": "USD",
        "tiers": billing_service.TIERS
    }

@router.get("/invoice")
def generate_usage_invoice(tier: str = Query("pro"), total_calls: int = Query(12500)):
    """Calculate usage-based billing invoice for API key owner."""
    invoice = billing_service.calculate_invoice(tier, total_calls)
    return {
        "status": "success",
        "invoice": invoice
    }
