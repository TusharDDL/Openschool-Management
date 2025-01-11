from typing import List, Optional, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from fastapi import HTTPException, status
from app.models.student import (
    StudentProfile, Guardian, StudentDocument,
    StudentNote, StudentAttendance
)
from app.models.academic_core import StudentSection
from app.schemas.student import (
    StudentProfileCreate, StudentProfileUpdate,
    GuardianCreate, GuardianUpdate,
    StudentDocumentCreate, StudentNoteCreate
)
from app.core.cache import CacheService
from app.core.security import get_password_hash
from app.models.user import User, UserRole

cache = CacheService()

# Student Profile CRUD
async def create_student(
    db: Session,
    tenant_id: int,
    data: StudentProfileCreate,
    created_by: int
) -> StudentProfile:
    # Create user account for student
    user = User(
        tenant_id=tenant_id,
        username=data.admission_number,
        email=f"{data.admission_number}@student.school",
        hashed_password=get_password_hash(data.admission_number),  # Temporary password
        role=UserRole.STUDENT,
        created_by=created_by
    )
    db.add(user)
    db.flush()  # Get user.id without committing

    # Create student profile
    profile_data = data.dict(exclude={'guardians'})
    profile = StudentProfile(
        tenant_id=tenant_id,
        user_id=user.id,
        **profile_data
    )
    db.add(profile)
    db.flush()  # Get profile.id without committing

    # Create guardians
    for guardian_data in data.guardians:
        guardian = Guardian(
            tenant_id=tenant_id,
            student_id=profile.id,
            **guardian_data.dict()
        )
        db.add(guardian)

    db.commit()
    db.refresh(profile)
    return profile

async def get_student(
    db: Session,
    tenant_id: int,
    student_id: int
) -> Optional[StudentProfile]:
    cache_key = f"student:{tenant_id}:{student_id}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return StudentProfile(**cached_data)
    
    student = db.query(StudentProfile).filter(
        and_(
            StudentProfile.tenant_id == tenant_id,
            StudentProfile.id == student_id
        )
    ).first()
    
    if student:
        cache.set(cache_key, student.__dict__, ttl=300)  # Cache for 5 minutes
    
    return student

async def get_students(
    db: Session,
    tenant_id: int,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    class_id: Optional[int] = None,
    section_id: Optional[int] = None,
    is_active: Optional[bool] = None
) -> List[StudentProfile]:
    query = db.query(StudentProfile).filter(StudentProfile.tenant_id == tenant_id)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                StudentProfile.first_name.ilike(search_term),
                StudentProfile.last_name.ilike(search_term),
                StudentProfile.admission_number.ilike(search_term)
            )
        )
    
    if class_id or section_id:
        query = query.join(StudentSection)
        if class_id:
            query = query.filter(StudentSection.class_id == class_id)
        if section_id:
            query = query.filter(StudentSection.section_id == section_id)
    
    if is_active is not None:
        query = query.filter(StudentProfile.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()

async def update_student(
    db: Session,
    tenant_id: int,
    student_id: int,
    data: StudentProfileUpdate
) -> Optional[StudentProfile]:
    student = await get_student(db, tenant_id, student_id)
    if not student:
        return None
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    
    # Invalidate cache
    cache.delete(f"student:{tenant_id}:{student_id}")
    
    return student

# Guardian CRUD
async def create_guardian(
    db: Session,
    tenant_id: int,
    student_id: int,
    data: GuardianCreate
) -> Guardian:
    guardian = Guardian(
        tenant_id=tenant_id,
        student_id=student_id,
        **data.dict()
    )
    db.add(guardian)
    db.commit()
    db.refresh(guardian)
    return guardian

async def update_guardian(
    db: Session,
    tenant_id: int,
    guardian_id: int,
    data: GuardianUpdate
) -> Optional[Guardian]:
    guardian = db.query(Guardian).filter(
        and_(
            Guardian.tenant_id == tenant_id,
            Guardian.id == guardian_id
        )
    ).first()
    
    if not guardian:
        return None
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(guardian, field, value)
    
    db.commit()
    db.refresh(guardian)
    return guardian

# Document Management
async def create_document(
    db: Session,
    tenant_id: int,
    data: StudentDocumentCreate,
    uploaded_by: int
) -> StudentDocument:
    document = StudentDocument(
        tenant_id=tenant_id,
        uploaded_by=uploaded_by,
        **data.dict()
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

async def verify_document(
    db: Session,
    tenant_id: int,
    document_id: int,
    verified_by: int
) -> Optional[StudentDocument]:
    document = db.query(StudentDocument).filter(
        and_(
            StudentDocument.tenant_id == tenant_id,
            StudentDocument.id == document_id
        )
    ).first()
    
    if not document:
        return None
    
    document.is_verified = True
    document.verified_by = verified_by
    document.verification_date = date.today()
    
    db.commit()
    db.refresh(document)
    return document

# Notes Management
async def create_note(
    db: Session,
    tenant_id: int,
    data: StudentNoteCreate,
    created_by: int
) -> StudentNote:
    note = StudentNote(
        tenant_id=tenant_id,
        created_by=created_by,
        **data.dict()
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

async def get_student_notes(
    db: Session,
    tenant_id: int,
    student_id: int,
    note_type: Optional[str] = None
) -> List[StudentNote]:
    query = db.query(StudentNote).filter(
        and_(
            StudentNote.tenant_id == tenant_id,
            StudentNote.student_id == student_id
        )
    )
    
    if note_type:
        query = query.filter(StudentNote.note_type == note_type)
    
    return query.order_by(desc(StudentNote.created_at)).all()

# Attendance Summary
async def get_attendance_summary(
    db: Session,
    tenant_id: int,
    student_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> Dict[str, Any]:
    query = db.query(
        func.count().label('total_days'),
        func.sum(StudentAttendance.status == 'present').label('present_days'),
        func.sum(StudentAttendance.status == 'absent').label('absent_days'),
        func.sum(StudentAttendance.status == 'late').label('late_days'),
        func.sum(StudentAttendance.status == 'excused').label('excused_days')
    ).filter(
        and_(
            StudentAttendance.tenant_id == tenant_id,
            StudentAttendance.student_id == student_id
        )
    )
    
    if start_date:
        query = query.filter(StudentAttendance.date >= start_date)
    if end_date:
        query = query.filter(StudentAttendance.date <= end_date)
    
    result = query.first()
    
    if not result or not result.total_days:
        return {
            'total_days': 0,
            'present_days': 0,
            'absent_days': 0,
            'late_days': 0,
            'excused_days': 0,
            'attendance_percentage': 0.0
        }
    
    attendance_percentage = (
        (result.present_days + result.late_days) / result.total_days
    ) * 100
    
    return {
        'total_days': result.total_days,
        'present_days': result.present_days,
        'absent_days': result.absent_days,
        'late_days': result.late_days,
        'excused_days': result.excused_days,
        'attendance_percentage': round(attendance_percentage, 2)
    }

# Utility Functions
async def get_student_current_section(
    db: Session,
    tenant_id: int,
    student_id: int
) -> Optional[Dict[str, Any]]:
    cache_key = f"student_section:{tenant_id}:{student_id}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    result = db.query(
        StudentSection.section_id,
        StudentSection.roll_number
    ).filter(
        and_(
            StudentSection.tenant_id == tenant_id,
            StudentSection.student_id == student_id,
            StudentSection.is_active == True
        )
    ).first()
    
    if result:
        data = {
            'section_id': result.section_id,
            'roll_number': result.roll_number
        }
        cache.set(cache_key, data, ttl=3600)  # Cache for 1 hour
        return data
    
    return None
