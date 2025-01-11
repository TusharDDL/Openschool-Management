from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
    AttendanceReport
)
from app.services import attendance as attendance_service

router = APIRouter()

@router.post("/", response_model=AttendanceResponse)
async def mark_attendance(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    attendance_data: AttendanceCreate
):
    """Mark attendance for a student"""
    return await attendance_service.mark_attendance(
        db=db,
        attendance_data=attendance_data,
        marked_by=current_user.id
    )

@router.get("/student/{student_id}", response_model=List[AttendanceResponse])
async def get_student_attendance(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    student_id: int,
    start_date: date,
    end_date: date
):
    """Get attendance records for a student"""
    return await attendance_service.get_student_attendance(
        db=db,
        student_id=student_id,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/class/{class_id}", response_model=List[AttendanceResponse])
async def get_class_attendance(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    class_id: int,
    date: date
):
    """Get attendance records for a class on a specific date"""
    return await attendance_service.get_class_attendance(
        db=db,
        class_id=class_id,
        date=date
    )

@router.put("/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    attendance_id: int,
    attendance_data: AttendanceUpdate
):
    """Update an attendance record"""
    return await attendance_service.update_attendance(
        db=db,
        attendance_id=attendance_id,
        attendance_data=attendance_data,
        updated_by=current_user.id
    )

@router.get("/report", response_model=AttendanceReport)
async def get_attendance_report(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    class_id: int,
    start_date: date,
    end_date: date
):
    """Get attendance report for a class"""
    return await attendance_service.get_attendance_report(
        db=db,
        class_id=class_id,
        start_date=start_date,
        end_date=end_date
    )