from fastapi import APIRouter
from app.core.config import get_settings
from app.api.api_v1.endpoints import (
    auth, schools, tenants, students, academic, fees,
    attendance, subjects, timetable
)

settings = get_settings()
api_router = APIRouter(prefix=settings.API_V1_STR)

# Include route modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(schools.router, prefix="/schools", tags=["Schools"])
api_router.include_router(students.router, prefix="/students", tags=["Students"])
api_router.include_router(academic.router, prefix="/academic", tags=["Academic"])
api_router.include_router(timetable.router, prefix="/academic", tags=["Academic"])
api_router.include_router(fees.router, prefix="/fees", tags=["Fees"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
api_router.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
