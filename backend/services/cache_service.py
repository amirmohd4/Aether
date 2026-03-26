import redis
import json
from typing import Any, Optional
from config import settings
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    """Redis caching service with fallback support"""
    
    def __init__(self):
        try:
            self.redis_client = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            self.available = True
            logger.info("✅ Redis connection established")
        except Exception as e:
            logger.warning(f"⚠️  Redis unavailable: {e}. Running without cache.")
            self.available = False
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.available:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis GET error for key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        """Set value in cache with TTL (default 5 minutes)"""
        if not self.available:
            return False
        
        try:
            serialized = json.dumps(value, default=str)
            self.redis_client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.error(f"Redis SET error for key {key}: {e}")
            return False
    
    def delete(self, key: str):
        """Delete key from cache"""
        if not self.available:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis DELETE error for key {key}: {e}")
            return False
    
    def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern"""
        if not self.available:
            return False
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Redis CLEAR PATTERN error for {pattern}: {e}")
            return False
    
    def health_check(self) -> dict:
        """Check Redis health status"""
        if not self.available:
            return {"status": "unavailable", "message": "Redis not connected"}
        
        try:
            self.redis_client.ping()
            return {"status": "healthy", "message": "Redis operational"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

# Global cache instance
cache = RedisCache()
