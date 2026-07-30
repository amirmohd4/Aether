import time
import secrets
from typing import Dict, Any, Optional

class ApiKeyModel:
    """In-memory or ORM model for API Keys in Aether Developer Portal."""
    def __init__(self, owner: str, tier: str = "free", custom_rate_limit: int = 100):
        self.key_id = f"aeth_live_{secrets.token_hex(16)}"
        self.owner = owner
        self.tier = tier
        self.rate_limit = custom_rate_limit if custom_rate_limit else self._get_tier_limit(tier)
        self.usage_count = 0
        self.created_at = int(time.time())
        self.expires_at = self.created_at + (365 * 86400)  # 1 year
        self.is_active = True

    def _get_tier_limit(self, tier: str) -> int:
        limits = {
            "free": 100,
            "starter": 10000,
            "pro": 50000,
            "enterprise": 1000000
        }
        return limits.get(tier.lower(), 100)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "owner": self.owner,
            "tier": self.tier,
            "rate_limit": self.rate_limit,
            "usage_count": self.usage_count,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "is_active": self.is_active
        }
