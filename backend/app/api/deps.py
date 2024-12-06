from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import BaseModel
import time
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.core.auth import oauth2_scheme
from app.core.cache import CacheService

settings = get_settings()
cache = CacheService()

class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 50
    order_by: Optional[str] = None
    order_dir: Optional[str] = "asc"

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    @property
    def limit(self) -> int:
        return self.per_page

class RateLimiter:
    def __init__(self, requests: int = 100, window: int = 60):
        self.requests = requests
        self.window = window
        self.cache = CacheService()

    async def is_rate_limited(self, key: str) -> bool:
        current = int(time.time())
        window_key = f"{key}:{current // self.window}"
        count = self.cache.get(window_key) or 0
        
        if count >= self.requests:
            return True
        
        self.cache.set(window_key, count + 1, ttl=self.window)
        return False

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_pagination(
    page: int = 1,
    per_page: int = 50,
    order_by: Optional[str] = None,
    order_dir: Optional[str] = "asc"
) -> PaginationParams:
    return PaginationParams(
        page=page,
        per_page=per_page,
        order_by=order_by,
        order_dir=order_dir
    )

rate_limiter = RateLimiter()

async def check_rate_limit(request: Request):
    client_ip = request.client.host
    school_id = request.state.school_id if hasattr(request.state, "school_id") else "anonymous"
    key = f"rate_limit:{client_ip}:{school_id}"
    
    if await rate_limiter.is_rate_limited(key):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )
    return True

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get user from cache first
    cache_key = f"user:{user_id}"
    user = cache.get(cache_key)
    if not user:
        # Query database if not in cache
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            cache.set(cache_key, user.dict(), ttl=300)  # Cache for 5 minutes
    
    if not user:
        raise credentials_exception
        
    return user