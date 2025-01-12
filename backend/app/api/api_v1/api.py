from fastapi import APIRouter
from app.core.config import get_settings
from app.api.api_v1.endpoints import (
    auth, schools, tenants, students, academic, fees,
    attendance, subjects, timetable
)
from app.api.api_v1.endpoints.parent import router as parent_router
from app.api.api_v1.endpoints.support import router as support_router
from app.api.api_v1.endpoints.stats import router as stats_router
from app.api.api_v1.endpoints.monitoring import router as monitoring_router

settings = get_settings()
api_router = APIRouter()

# Include route modules
# Routes will be prefixed with settings.API_V1_STR in main.py
# Do not add prefix here as it's handled in main.py
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(schools.router, prefix="/schools", tags=["Schools"])
api_router.include_router(students.router, prefix="/students", tags=["Students"])
api_router.include_router(academic.router, prefix="/academic", tags=["Academic"])
api_router.include_router(timetable.router, prefix="/academic", tags=["Academic"])
api_router.include_router(fees.router, prefix="/fees", tags=["Fees"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
api_router.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
api_router.include_router(parent_router, prefix="/parent", tags=["Parent"])
api_router.include_router(support_router, prefix="/support", tags=["Support"])
api_router.include_router(stats_router, tags=["Stats"])
api_router.include_router(monitoring_router, prefix="/monitoring", tags=["Monitoring"])
