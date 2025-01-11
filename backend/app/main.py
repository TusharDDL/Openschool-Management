# File: backend/app/main.py
# Main FastAPI application entry point

import json
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

from app.core.config import get_settings
from app.core.middleware import LoggingMiddleware, RequestValidationMiddleware
from app.api.api_v1.api import api_router
from app.core.database import Base, engine

settings = get_settings()

# Create database tables
from app.db.init_db import init_db
from app.core.database import SessionLocal

# Initialize database
db = SessionLocal()
init_db(db)
Base.metadata.create_all(bind=engine)
db.close()

from fastapi.encoders import jsonable_encoder

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for School Management System",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestValidationMiddleware)

# Include API router
app.include_router(api_router)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/")
async def root():
    return JSONResponse(
        content={
            "message": "Welcome to School Management API",
            "version": settings.VERSION,
            "docs": "/docs",
            "status": "operational"
        }
    )

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}