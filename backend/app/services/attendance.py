from typing import List, Dict, Optional
from datetime import date, time
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from fastapi import HTTPException, status

from app.models.student import StudentAttendance
from app.models.student import StudentProfile
from app.models.academic_core import Class, Section
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceReport,
    StudentAttendanceSummary
)

async def mark_attendance(
    db: Session,
    attendance_data: AttendanceCreate,
    marked_by: int
) -> StudentAttendance:
    """Mark attendance for a student"""
    # Verify student exists and belongs to the class
    student = db.query(StudentProfile).filter(
        StudentProfile.id == attendance_data.student_id
    ).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Check if attendance already marked
    existing_attendance = db.query(StudentAttendance).filter(
        and_(
            StudentAttendance.student_id == attendance_data.student_id,
            StudentAttendance.date == attendance_data.date
        )
    ).first()
    if existing_attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already marked for this student on this date"
        )

    # Create attendance record
    attendance = StudentAttendance(
        **attendance_data.model_dump(),
        marked_by=marked_by
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

async def get_student_attendance(
    db: Session,
    student_id: int,
    start_date: date,
    end_date: date
) -> List[StudentAttendance]:
    """Get attendance records for a student"""
    return db.query(StudentAttendance).filter(
        and_(
            StudentAttendance.student_id == student_id,
            StudentAttendance.date.between(start_date, end_date)
        )
    ).order_by(StudentAttendance.date.desc()).all()

async def get_class_attendance(
    db: Session,
    class_id: int,
    date: date
) -> List[StudentAttendance]:
    """Get attendance records for a class on a specific date"""
    return db.query(StudentAttendance).join(
        StudentProfile
    ).filter(
        and_(
            StudentAttendance.class_id == class_id,
            StudentAttendance.date == date
        )
    ).order_by(StudentProfile.first_name).all()

async def update_attendance(
    db: Session,
    attendance_id: int,
    attendance_data: AttendanceUpdate,
    updated_by: int
) -> StudentAttendance:
    """Update an attendance record"""
    attendance = db.query(StudentAttendance).filter(
        StudentAttendance.id == attendance_id
    ).first()
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )

    # Update fields
    for field, value in attendance_data.model_dump(exclude_unset=True).items():
        setattr(attendance, field, value)
    attendance.marked_by = updated_by

    db.commit()
    db.refresh(attendance)
    return attendance

async def get_attendance_report(
    db: Session,
    class_id: int,
    start_date: date,
    end_date: date
) -> AttendanceReport:
    """Get attendance report for a class"""
    # Get class details
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    # Get all students in the class
    students = db.query(StudentProfile).join(
        Section
    ).filter(
        Section.class_id == class_id
    ).all()

    # Calculate working days
    total_working_days = (end_date - start_date).days + 1

    # Get attendance summaries for each student
    student_summaries = []
    daily_attendance = {}

    for student in students:
        # Get attendance records
        attendance_records = db.query(StudentAttendance).filter(
            and_(
                StudentAttendance.student_id == student.id,
                StudentAttendance.date.between(start_date, end_date)
            )
        ).all()

        # Count statuses
        status_counts = {
            "present": 0,
            "absent": 0,
            "late": 0,
            "excused": 0
        }
        for record in attendance_records:
            status_counts[record.status.lower()] += 1
            
            # Add to daily attendance
            date_str = record.date.isoformat()
            if date_str not in daily_attendance:
                daily_attendance[date_str] = {}
            daily_attendance[date_str][student.id] = record.status

        # Calculate percentage
        total_present = status_counts["present"] + status_counts["late"]
        attendance_percentage = (total_present / total_working_days) * 100 if total_working_days > 0 else 0

        student_summaries.append(StudentAttendanceSummary(
            student_id=student.id,
            student_name=f"{student.first_name} {student.last_name}",
            total_days=total_working_days,
            present_days=status_counts["present"],
            absent_days=status_counts["absent"],
            late_days=status_counts["late"],
            excused_days=status_counts["excused"],
            attendance_percentage=round(attendance_percentage, 2)
        ))

    return AttendanceReport(
        class_id=class_id,
        class_name=class_.name,
        start_date=start_date,
        end_date=end_date,
        total_working_days=total_working_days,
        student_summaries=student_summaries,
        daily_attendance=daily_attendance
    )