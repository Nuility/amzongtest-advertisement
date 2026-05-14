import redis
import json
import logging
from typing import Optional, Any, List
from app.core.config import get_settings
import random

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self):
        settings = get_settings()
        try:
            self.client = redis.from_url(
                settings.redis_url,
                max_connections=settings.redis_max_connections,
                socket_timeout=settings.redis_socket_timeout,
                decode_responses=True
            )
            self.client.ping()
            logger.info("Redis cache service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None
    
    def get(self, key: str) -> Optional[Any]:
        if not self.client:
            logger.debug("Cache unavailable, returning None")
            return None
        
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None, randomize_ttl: bool = True) -> bool:
        if not self.client:
            logger.debug("Cache unavailable, skipping set")
            return False
        
        try:
            settings = get_settings()
            actual_ttl = ttl or settings.cache_default_ttl
            
            if randomize_ttl:
                actual_ttl = int(actual_ttl * random.uniform(0.8, 1.2))
            
            serialized = json.dumps(value)
            self.client.setex(key, actual_ttl, serialized)
            return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        if not self.client:
            return False
        
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    def invalidate_pattern(self, pattern: str) -> int:
        if not self.client:
            return 0
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Cache invalidate pattern error for pattern {pattern}: {e}")
            return 0
    
    @staticmethod
    def build_key(prefix: str, *args) -> str:
        return f"{prefix}:{':'.join(str(arg) for arg in args)}"
    
    @staticmethod
    def build_pattern(prefix: str, *args) -> str:
        return f"{prefix}:{':'.join(str(arg) for arg in args)}*"


cache_service = CacheService()


def get_cache() -> CacheService:
    return cache_service
