from fastapi import APIRouter
from app.api.v1 import academic

api_router = APIRouter()

api_router.include_router(academic.router, prefix="/academic", tags=["academic"])