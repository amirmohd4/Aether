from __future__ import annotations

from typing import Any, Dict


def marketplace_catalog(registry) -> Dict[str, Any]:
    """Expose every MVP service as a sandbox developer API contract."""
    apis = []
    for service in registry.all():
        apis.append({
            "service_id": service.id,
            "name": service.name,
            "department": service.department,
            "customer_types": service.customer_types,
            "outcome": service.outcome,
            "endpoint": "/api/aether/v2/cases",
            "authentication": "Supabase Auth or tenant API key",
            "sandbox": True,
            "live_connector_required": True,
            "pricing": {
                "model": "contract_or_usage",
                "currency": "INR",
                "price_minor": None,
            },
        })
    return {
        "status": "success",
        "environment": "sandbox",
        "apis": apis,
        "count": len(apis),
        "note": "Sandbox catalog only. It does not itself grant government authority or live connector access.",
    }
