from typing import Dict, Any, List

class BillingService:
    TIERS = {
        "free": {"name": "Free Tier", "price_usd": 0, "included_requests": 100, "overage_rate": 0.00},
        "starter": {"name": "Starter Tier", "price_usd": 99, "included_requests": 10000, "overage_rate": 0.01},
        "pro": {"name": "Pro Tier", "price_usd": 499, "included_requests": 50000, "overage_rate": 0.008},
        "enterprise": {"name": "Enterprise Sovereign", "price_usd": 2500, "included_requests": 500000, "overage_rate": 0.005}
    }

    @classmethod
    def calculate_invoice(cls, tier_name: str, total_calls: int) -> Dict[str, Any]:
        tier = cls.TIERS.get(tier_name.lower(), cls.TIERS["free"])
        base_price = tier["price_usd"]
        included = tier["included_requests"]
        overage_rate = tier["overage_rate"]
        
        extra_calls = max(0, total_calls - included)
        overage_fee = round(extra_calls * overage_rate, 2)
        total_due = round(base_price + overage_fee, 2)
        
        return {
            "tier": tier["name"],
            "base_subscription_usd": base_price,
            "included_requests": included,
            "actual_requests_used": total_calls,
            "extra_requests": extra_calls,
            "overage_fee_usd": overage_fee,
            "total_due_usd": total_due,
            "breakdown": [
                {"description": f"{tier['name']} Monthly Subscription", "amount_usd": base_price},
                {"description": f"Overage Usage ({extra_calls} calls @ ${overage_rate}/call)", "amount_usd": overage_fee}
            ]
        }

billing_service = BillingService()
