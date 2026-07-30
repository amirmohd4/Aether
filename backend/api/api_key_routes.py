from fastapi import APIRouter, HTTPException, Header, Body
from typing import Dict, Any, Optional
from backend.models.api_key import ApiKeyModel

router = APIRouter(prefix="/api/v1/developer/keys", tags=["Private Sector API Portal"])

# Simulated persistent store for developer API keys
API_KEYS_DB: Dict[str, ApiKeyModel] = {}

# Seed default developer keys
demo_key = ApiKeyModel(owner="Standard Chartered Bank API Client", tier="pro", custom_rate_limit=50000)
demo_key.key_id = "aeth_live_bank_demo_key_9988"
API_KEYS_DB[demo_key.key_id] = demo_key

@router.post("/generate")
def generate_api_key(payload: Dict[str, Any] = Body(...)):
    """Generate a new API key for private sector institutional access (Banks, Insurers, Conveyancers)."""
    owner = payload.get("owner")
    tier = payload.get("tier", "free")
    
    if not owner:
        raise HTTPException(status_code=400, detail="Owner name or Organization email is required")
        
    api_key = ApiKeyModel(owner=owner, tier=tier)
    API_KEYS_DB[api_key.key_id] = api_key
    
    return {
        "status": "success",
        "message": f"API key generated for {owner}",
        "api_key": api_key.to_dict()
    }

@router.get("/list")
def list_api_keys(owner: Optional[str] = None):
    """Retrieve active API keys for an organization."""
    results = [k.to_dict() for k in API_KEYS_DB.values() if owner is None or k.owner.lower() == owner.lower()]
    return {"status": "success", "count": len(results), "keys": results}

@router.post("/revoke/{key_id}")
def revoke_api_key(key_id: str):
    """Revoke an existing API key immediately."""
    if key_id not in API_KEYS_DB:
        raise HTTPException(status_code=404, detail="API key not found")
        
    API_KEYS_DB[key_id].is_active = False
    return {"status": "success", "message": f"API Key {key_id} revoked successfully"}
