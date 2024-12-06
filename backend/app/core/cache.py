from typing import Any, Optional
from redis import Redis
import json
from functools import wraps
import hashlib
from app.core.config import settings

class CacheService:
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.default_ttl = 3600  # 1 hour

    def _get_key(self, prefix: str, *args, **kwargs) -> str:
        key_parts = [prefix]
        if args:
            key_parts.extend([str(arg) for arg in args])
        if kwargs:
            key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
        key = ":".join(key_parts)
        return hashlib.md5(key.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        data = json.dumps(value)
        self.redis.set(key, data, ex=ttl or self.default_ttl)

    def delete(self, key: str) -> None:
        self.redis.delete(key)

    def clear_prefix(self, prefix: str) -> None:
        keys = self.redis.keys(f"{prefix}:*")
        if keys:
            self.redis.delete(*keys)

def cached(prefix: str, ttl: Optional[int] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = CacheService()
            cache_key = cache._get_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # If not in cache, execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Usage example:
"""
@cached("student_profile", ttl=1800)
async def get_student_profile(student_id: int, school_id: int):
    return await db.fetch_one(
        "SELECT * FROM students WHERE id = :id AND school_id = :school_id",
        {"id": student_id, "school_id": school_id}
    )
"""