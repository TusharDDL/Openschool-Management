from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, check_rate_limit
from app.core.security import require_school_admin, require_teacher
from app.schemas.academic import (
    AcademicYear, AcademicYearCreate, AcademicYearUpdate,
    Class, ClassCreate, ClassUpdate,
    Section, SectionCreate, SectionUpdate,
    Subject, SubjectCreate, SubjectUpdate,
    StudentSection, StudentSectionCreate,
    TeacherSection, TeacherSectionCreate
)
from app.crud import academic as crud_academic
from app.models.user import User

router = APIRouter()

# Academic Year routes
@router.post("/years", response_model=AcademicYear, status_code=status.HTTP_201_CREATED)
async def create_academic_year(
    data: AcademicYearCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Create a new academic year (requires school_admin role)"""
    return crud_academic.create_academic_year(db, current_user.tenant_id, data)

@router.get("/years", response_model=List[AcademicYear])
async def list_academic_years(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """List academic years"""
    return crud_academic.get_academic_years(
        db,
        current_user.tenant_id,
        skip=skip,
        limit=limit,
        is_active=is_active
    )

@router.get("/years/{year_id}", response_model=AcademicYear)
async def get_academic_year_by_id(
    year_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Get academic year by ID"""
    db_obj = crud_academic.get_academic_year(db, current_user.tenant_id, year_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic year not found"
        )
    return db_obj

@router.put("/years/{year_id}", response_model=AcademicYear)
async def update_academic_year(
    year_id: int,
    data: AcademicYearUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Update academic year (requires school_admin role)"""
    db_obj = crud_academic.update_academic_year(
        db,
        current_user.tenant_id,
        year_id,
        data
    )
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic year not found"
        )
    return db_obj

# Class routes
@router.post("/classes", response_model=Class, status_code=status.HTTP_201_CREATED)
async def create_class(
    data: ClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Create a new class (requires school_admin role)"""
    return crud_academic.create_class(db, current_user.tenant_id, data)

@router.get("/classes", response_model=List[Class])
async def list_classes(
    academic_year_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """List classes"""
    return crud_academic.get_classes(
        db,
        current_user.tenant_id,
        academic_year_id=academic_year_id,
        skip=skip,
        limit=limit,
        is_active=is_active
    )

@router.get("/classes/{class_id}", response_model=Class)
async def get_class_by_id(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Get class by ID"""
    db_obj = crud_academic.get_class(db, current_user.tenant_id, class_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    return db_obj

@router.put("/classes/{class_id}", response_model=Class)
async def update_class(
    class_id: int,
    data: ClassUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Update class (requires school_admin role)"""
    db_obj = crud_academic.update_class(
        db,
        current_user.tenant_id,
        class_id,
        data
    )
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    return db_obj

# Section routes
@router.post("/sections", response_model=Section, status_code=status.HTTP_201_CREATED)
async def create_section(
    data: SectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Create a new section (requires school_admin role)"""
    return crud_academic.create_section(db, current_user.tenant_id, data)

@router.get("/sections", response_model=List[Section])
async def list_sections(
    class_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """List sections"""
    return crud_academic.get_sections(
        db,
        current_user.tenant_id,
        class_id=class_id,
        skip=skip,
        limit=limit,
        is_active=is_active
    )

@router.get("/sections/{section_id}", response_model=Section)
async def get_section_by_id(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Get section by ID"""
    db_obj = crud_academic.get_section(db, current_user.tenant_id, section_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    return db_obj

@router.put("/sections/{section_id}", response_model=Section)
async def update_section(
    section_id: int,
    data: SectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Update section (requires school_admin role)"""
    db_obj = crud_academic.update_section(
        db,
        current_user.tenant_id,
        section_id,
        data
    )
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    return db_obj

# Student Section Assignment routes
@router.post("/student-sections", response_model=StudentSection, status_code=status.HTTP_201_CREATED)
async def assign_student_to_section(
    data: StudentSectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Assign a student to a section (requires school_admin role)"""
    return crud_academic.assign_student_to_section(
        db,
        current_user.tenant_id,
        data
    )

# Teacher Section Assignment routes
@router.post("/teacher-sections", response_model=TeacherSection, status_code=status.HTTP_201_CREATED)
async def assign_teacher_to_section(
    data: TeacherSectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Assign a teacher to a section (requires school_admin role)"""
    return crud_academic.assign_teacher_to_section(
        db,
        current_user.tenant_id,
        data
    )

# Utility routes
@router.get("/classes/{class_id}/students")
async def get_class_students(
    class_id: int,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
    _: bool = Depends(check_rate_limit)
):
    """Get all students in a class (requires teacher role)"""
    return crud_academic.get_class_students(
        db,
        current_user.tenant_id,
        class_id,
        is_active=is_active
    )

@router.get("/teachers/{teacher_id}/classes")
async def get_teacher_classes(
    teacher_id: int,
    academic_year_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Get all classes assigned to a teacher"""
    # Only allow teachers to view their own classes or admins to view any teacher's classes
    if current_user.role != "school_admin" and current_user.id != teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view other teacher's classes"
        )
    
    return crud_academic.get_teacher_classes(
        db,
        current_user.tenant_id,
        teacher_id,
        academic_year_id=academic_year_id
    )
