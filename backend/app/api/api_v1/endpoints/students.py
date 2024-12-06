from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, check_rate_limit
from app.core.security import require_school_admin, require_teacher
from app.schemas.student import (
    StudentProfile, StudentProfileCreate, StudentProfileUpdate,
    Guardian, GuardianCreate, GuardianUpdate,
    StudentDocument, StudentDocumentCreate,
    StudentNote, StudentNoteCreate,
    StudentBasicInfo, StudentDetailedInfo,
    StudentAttendanceSummary
)
from app.crud import student as crud_student
from app.models.user import User
from app.core.storage import upload_file_to_s3

router = APIRouter()

# Student Profile Routes
@router.post("/", response_model=StudentProfile)
async def create_student(
    data: StudentProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Create a new student profile (requires school_admin role)"""
    return await crud_student.create_student(
        db,
        current_user.tenant_id,
        data,
        current_user.id
    )

@router.get("/", response_model=List[StudentBasicInfo])
async def list_students(
    search: Optional[str] = None,
    class_id: Optional[int] = None,
    section_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """List students with optional filtering"""
    return await crud_student.get_students(
        db,
        current_user.tenant_id,
        skip=skip,
        limit=limit,
        search=search,
        class_id=class_id,
        section_id=section_id,
        is_active=is_active
    )

@router.get("/{student_id}", response_model=StudentDetailedInfo)
async def get_student_by_id(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Get detailed student information"""
    student = await crud_student.get_student(db, current_user.tenant_id, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Get additional information
    attendance_summary = await crud_student.get_attendance_summary(
        db,
        current_user.tenant_id,
        student_id
    )
    
    section_info = await crud_student.get_student_current_section(
        db,
        current_user.tenant_id,
        student_id
    )
    
    return {
        **student.__dict__,
        "attendance_summary": attendance_summary,
        "current_section": section_info.get("section_name") if section_info else None,
        "current_class": section_info.get("class_name") if section_info else None,
        "academic_year": section_info.get("academic_year") if section_info else None
    }

@router.put("/{student_id}", response_model=StudentProfile)
async def update_student(
    student_id: int,
    data: StudentProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Update student profile (requires school_admin role)"""
    student = await crud_student.update_student(
        db,
        current_user.tenant_id,
        student_id,
        data
    )
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

# Guardian Routes
@router.post("/{student_id}/guardians", response_model=Guardian)
async def add_guardian(
    student_id: int,
    data: GuardianCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Add a guardian to a student (requires school_admin role)"""
    # Verify student exists
    student = await crud_student.get_student(db, current_user.tenant_id, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return await crud_student.create_guardian(
        db,
        current_user.tenant_id,
        student_id,
        data
    )

@router.put("/guardians/{guardian_id}", response_model=Guardian)
async def update_guardian(
    guardian_id: int,
    data: GuardianUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Update guardian information (requires school_admin role)"""
    guardian = await crud_student.update_guardian(
        db,
        current_user.tenant_id,
        guardian_id,
        data
    )
    if not guardian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guardian not found"
        )
    return guardian

# Document Routes
@router.post("/{student_id}/documents", response_model=StudentDocument)
async def upload_document(
    student_id: int,
    document_type: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Upload a document for a student (requires school_admin role)"""
    # Verify student exists
    student = await crud_student.get_student(db, current_user.tenant_id, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Upload file to S3
    file_url = await upload_file_to_s3(
        file,
        f"students/{student_id}/documents/{document_type}/{file.filename}"
    )
    
    document_data = StudentDocumentCreate(
        student_id=student_id,
        document_type=document_type,
        file_name=file.filename,
        file_size=file.size,
        mime_type=file.content_type,
        document_url=file_url
    )
    
    return await crud_student.create_document(
        db,
        current_user.tenant_id,
        document_data,
        current_user.id
    )

@router.post("/documents/{document_id}/verify", response_model=StudentDocument)
async def verify_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Verify a student document (requires school_admin role)"""
    document = await crud_student.verify_document(
        db,
        current_user.tenant_id,
        document_id,
        current_user.id
    )
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document

# Notes Routes
@router.post("/{student_id}/notes", response_model=StudentNote)
async def add_note(
    student_id: int,
    data: StudentNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
    _: bool = Depends(check_rate_limit)
):
    """Add a note to a student (requires teacher role)"""
    # Verify student exists
    student = await crud_student.get_student(db, current_user.tenant_id, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return await crud_student.create_note(
        db,
        current_user.tenant_id,
        data,
        current_user.id
    )

@router.get("/{student_id}/notes", response_model=List[StudentNote])
async def get_student_notes(
    student_id: int,
    note_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
    _: bool = Depends(check_rate_limit)
):
    """Get student notes (requires teacher role)"""
    # Verify student exists
    student = await crud_student.get_student(db, current_user.tenant_id, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return await crud_student.get_student_notes(
        db,
        current_user.tenant_id,
        student_id,
        note_type
    )

# Attendance Routes
@router.get("/{student_id}/attendance", response_model=StudentAttendanceSummary)
async def get_attendance_summary(
    student_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Get student attendance summary"""
    # Verify student exists
    student = await crud_student.get_student(db, current_user.tenant_id, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return await crud_student.get_attendance_summary(
        db,
        current_user.tenant_id,
        student_id,
        start_date,
        end_date
    )
