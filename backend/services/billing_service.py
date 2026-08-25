from typing import Dict, Any, List
from datetime import datetime, timedelta

class BillingService:
    TIERS = {
        "free": {"name": "Free Tier", "price_usd": 0, "included_requests": 100, "per_request_rate": 0.00},
        "starter": {"name": "Starter Tier", "price_usd": 99, "included_requests": 10000, "per_request_rate": 0.01},
        "pro": {"name": "Pro Tier", "price_usd": 499, "included_requests": 50000, "per_request_rate": 0.005},
        "enterprise": {"name": "Enterprise Sovereign", "price_usd": 2500, "included_requests": 500000, "per_request_rate": 0.005}
    }

    @classmethod
    def calculate_invoice(cls, tier_name: str, total_calls: int) -> Dict[str, Any]:
        tier = cls.TIERS.get(tier_name.lower(), cls.TIERS["free"])
        base_price = tier["price_usd"]
        included = tier["included_requests"]
        rate = tier["per_request_rate"]

        extra_calls = max(0, total_calls - included)
        extra_cost = extra_calls * rate

        total = base_price + extra_cost

        return {
            "tier": tier["name"],
            "base_price": base_price,
            "included_requests": included,
            "total_calls": total_calls,
            "extra_calls": extra_calls,
            "extra_cost": round(extra_cost, 2),
            "total_amount": round(total, 2),
            "currency": "USD",
            "generated_at": datetime.now().isoformat()
        }

    @classmethod
    def get_tier_details(cls, tier_name: str) -> Dict[str, Any]:
        tier = cls.TIERS.get(tier_name.lower())
        if tier:
            return {**tier, "tier_name": tier_name}
        return {"error": "Tier not found"}

# Singleton instance
billing_service = BillingService()
