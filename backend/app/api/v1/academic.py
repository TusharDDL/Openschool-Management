from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.crud import academic as crud
from app.schemas.academic import (
    AcademicYearCreate, AcademicYear,
    ClassCreate, Class,
    SectionCreate, Section,
    SubjectCreate, Subject,
    StudentSectionCreate, StudentSection,
    TeacherSectionCreate, TeacherSection
)

router = APIRouter()

# Academic Year endpoints
@router.post("/years", response_model=AcademicYear, status_code=status.HTTP_201_CREATED)
def create_academic_year(
    data: AcademicYearCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_academic_year(db, current_user.tenant_id, data)

@router.get("/years/{year_id}", response_model=AcademicYear)
def get_academic_year(
    year_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_obj = crud.get_academic_year(db, current_user.tenant_id, year_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic year not found"
        )
    return db_obj

# Class endpoints
@router.post("/classes", response_model=Class, status_code=status.HTTP_201_CREATED)
def create_class(
    data: ClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_class(db, current_user.tenant_id, data)

@router.get("/classes/{class_id}", response_model=Class)
def get_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_obj = crud.get_class(db, current_user.tenant_id, class_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    return db_obj

# Section endpoints
@router.post("/sections", response_model=Section, status_code=status.HTTP_201_CREATED)
def create_section(
    data: SectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_section(db, current_user.tenant_id, data)

@router.get("/sections/{section_id}", response_model=Section)
def get_section(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_obj = crud.get_section(db, current_user.tenant_id, section_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    return db_obj

# Subject endpoints
@router.post("/subjects", response_model=Subject, status_code=status.HTTP_201_CREATED)
def create_subject(
    data: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_subject(db, current_user.tenant_id, data)

@router.get("/subjects/{subject_id}", response_model=Subject)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_obj = crud.get_subject(db, current_user.tenant_id, subject_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return db_obj

# Student Section Assignment endpoints
@router.post("/student-sections", response_model=StudentSection, status_code=status.HTTP_201_CREATED)
def assign_student_to_section(
    data: StudentSectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.assign_student_to_section(db, current_user.tenant_id, data)

# Teacher Section Assignment endpoints
@router.post("/teacher-sections", response_model=TeacherSection, status_code=status.HTTP_201_CREATED)
def assign_teacher_to_section(
    data: TeacherSectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.assign_teacher_to_section(db, current_user.tenant_id, data)