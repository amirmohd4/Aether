from backend.config import settings
import redis
import json
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.redis_client = None
        self.enabled = settings.redis_enabled if hasattr(settings, 'redis_enabled') else False
        if self.enabled:
            try:
                self.redis_client = redis.Redis(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    db=settings.redis_db,
                    decode_responses=True
                )
                self.redis_client.ping()
                logger.info("Redis cache connected")
            except Exception as e:
                logger.error(f"Redis connection failed: {e}")
                self.enabled = False

    def get(self, key: str):
        if not self.enabled:
            return None
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: Any, expire: int = 300):
        if not self.enabled:
            return
        try:
            self.redis_client.setex(key, expire, json.dumps(value))
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    def delete(self, key: str):
        if not self.enabled:
            return
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")

# Singleton
cache = CacheService()
