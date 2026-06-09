"""Redis cache manager for fraud predictions."""
import json
import redis.asyncio as redis
from typing import Optional, Any
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class CacheManager:
    def __init__(self):
        self._redis: Optional[redis.Redis] = None

    async def connect(self):
        self._redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        await self._redis.ping()
        logger.info("redis_connected", url=settings.REDIS_URL)

    async def disconnect(self):
        if self._redis:
            await self._redis.close()

    async def get(self, key: str) -> Optional[Any]:
        if not self._redis:
            return None
        value = await self._redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: int = None):
        if not self._redis:
            return
        ttl = ttl or settings.REDIS_TTL
        await self._redis.setex(key, ttl, json.dumps(value))

    async def increment_counter(self, key: str, amount: int = 1) -> int:
        if not self._redis:
            return 0
        return await self._redis.incrby(key, amount)


cache_manager = CacheManager()
