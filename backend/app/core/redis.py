from redis import Redis
from app.core.config import settings
from functools import lru_cache

@lru_cache()
def get_redis_client() -> Redis:
    return Redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        socket_timeout=5,
        retry_on_timeout=True
    )

class RedisCache:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def get(self, key: str) -> str:
        return self.redis.get(key)

    async def set(
        self,
        key: str,
        value: str,
        expire: int = None
    ) -> bool:
        return self.redis.set(key, value, ex=expire)

    async def delete(self, key: str) -> bool:
        return self.redis.delete(key) > 0

    async def exists(self, key: str) -> bool:
        return self.redis.exists(key) > 0

    async def increment(self, key: str) -> int:
        return self.redis.incr(key)

    async def decrement(self, key: str) -> int:
        return self.redis.decr(key)