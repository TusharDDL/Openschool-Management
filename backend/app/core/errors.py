from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional
from sqlalchemy.exc import SQLAlchemyError
from redis.exceptions import RedisError

class AppError(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers

class DatabaseError(AppError):
    def __init__(self, detail: str = "Database error occurred"):
        super().__init__(status_code=500, detail=detail)

class CacheError(AppError):
    def __init__(self, detail: str = "Cache error occurred"):
        super().__init__(status_code=500, detail=detail)

class NotFoundError(AppError):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)

class ValidationError(AppError):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=422, detail=detail)

async def database_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred", "type": "database_error"}
    )

async def cache_error_handler(request: Request, exc: RedisError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "Cache error occurred", "type": "cache_error"}
    )

async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": exc.detail, "type": "validation_error"}
    )

async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": exc.detail, "type": "not_found"}
    )