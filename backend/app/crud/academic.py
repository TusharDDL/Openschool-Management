from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from fastapi import HTTPException, status
from app.models.academic_core import (
    AcademicYear, Class, Section, Subject,
    StudentSection, TeacherSection
)
from app.schemas.academic import (
    AcademicYearCreate, AcademicYearUpdate,
    ClassCreate, ClassUpdate,
    SectionCreate, SectionUpdate,
    SubjectCreate, SubjectUpdate,
    StudentSectionCreate, TeacherSectionCreate,
    TimetableCreate, TimetableUpdate,
    GradingSystemCreate, GradingSystemUpdate,
    AssessmentCreate, AssessmentUpdate,
    ResultCreate, ResultUpdate,
    TeacherNoteCreate, TeacherNoteUpdate
)
from app.core.cache import CacheService

cache = CacheService()

# Academic Year CRUD
def create_academic_year(db: Session, tenant_id: Optional[int], data: AcademicYearCreate) -> AcademicYear:
    data_dict = data.model_dump()
    data_dict["tenant_id"] = data_dict.get("tenant_id", tenant_id)
    db_obj = AcademicYear(**data_dict)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_academic_year(db: Session, tenant_id: int, year_id: int) -> Optional[AcademicYear]:
    cache_key = f"academic_year:{tenant_id}:{year_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return AcademicYear(**cached_data)
    
    db_obj = db.query(AcademicYear).filter(
        and_(
            AcademicYear.tenant_id == tenant_id,
            AcademicYear.id == year_id
        )
    ).first()
    
    if db_obj:
        cache.set(cache_key, db_obj.__dict__, ttl=3600)
    
    return db_obj

def get_academic_years(
    db: Session,
    tenant_id: int,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None
) -> List[AcademicYear]:
    query = db.query(AcademicYear).filter(AcademicYear.tenant_id == tenant_id)
    
    if is_active is not None:
        query = query.filter(AcademicYear.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()

def update_academic_year(
    db: Session,
    tenant_id: int,
    year_id: int,
    data: AcademicYearUpdate
) -> Optional[AcademicYear]:
    db_obj = get_academic_year(db, tenant_id, year_id)
    if not db_obj:
        return None
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    
    db.commit()
    db.refresh(db_obj)
    
    # Invalidate cache
    cache.delete(f"academic_year:{tenant_id}:{year_id}")
    
    return db_obj

# Class CRUD
def create_class(db: Session, tenant_id: Optional[int], data: ClassCreate) -> Class:
    # Use tenant_id from data if available, otherwise use the provided one
    actual_tenant_id = data.model_dump().get("tenant_id", tenant_id)
    
    # Verify academic year exists and belongs to tenant
    academic_year = db.query(AcademicYear).filter(
        AcademicYear.id == data.academic_year_id
    ).first()
    if not academic_year:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic year not found"
        )
    
    data_dict = data.model_dump()
    data_dict["tenant_id"] = actual_tenant_id
    db_obj = Class(**data_dict)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_class(db: Session, tenant_id: int, class_id: int) -> Optional[Class]:
    cache_key = f"class:{tenant_id}:{class_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return Class(**cached_data)
    
    db_obj = db.query(Class).filter(
        and_(
            Class.tenant_id == tenant_id,
            Class.id == class_id
        )
    ).first()
    
    if db_obj:
        cache.set(cache_key, db_obj.__dict__, ttl=3600)
    
    return db_obj

def get_classes(
    db: Session,
    tenant_id: int,
    academic_year_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None
) -> List[Class]:
    query = db.query(Class).filter(Class.tenant_id == tenant_id)
    
    if academic_year_id:
        query = query.filter(Class.academic_year_id == academic_year_id)
    
    if is_active is not None:
        query = query.filter(Class.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()

def update_class(
    db: Session,
    tenant_id: int,
    class_id: int,
    data: ClassUpdate
) -> Optional[Class]:
    db_obj = get_class(db, tenant_id, class_id)
    if not db_obj:
        return None
    
    # If academic year is being updated, verify it exists
    if data.academic_year_id:
        academic_year = get_academic_year(db, tenant_id, data.academic_year_id)
        if not academic_year:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Academic year not found"
            )
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    
    db.commit()
    db.refresh(db_obj)
    
    # Invalidate cache
    cache.delete(f"class:{tenant_id}:{class_id}")
    
    return db_obj

# Section CRUD
def create_section(db: Session, tenant_id: Optional[int], data: SectionCreate) -> Section:
    # Use tenant_id from data if available, otherwise use the provided one
    actual_tenant_id = data.model_dump().get("tenant_id", tenant_id)
    
    # Verify class exists
    class_obj = db.query(Class).filter(
        Class.id == data.class_id
    ).first()
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    data_dict = data.model_dump()
    data_dict["tenant_id"] = actual_tenant_id
    db_obj = Section(**data_dict)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_section(db: Session, tenant_id: int, section_id: int) -> Optional[Section]:
    cache_key = f"section:{tenant_id}:{section_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return Section(**cached_data)
    
    db_obj = db.query(Section).filter(
        and_(
            Section.tenant_id == tenant_id,
            Section.id == section_id
        )
    ).first()
    
    if db_obj:
        cache.set(cache_key, db_obj.__dict__, ttl=3600)
    
    return db_obj

def get_sections(
    db: Session,
    tenant_id: int,
    class_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None
) -> List[Section]:
    query = db.query(Section).filter(Section.tenant_id == tenant_id)
    
    if class_id:
        query = query.filter(Section.class_id == class_id)
    
    if is_active is not None:
        query = query.filter(Section.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()

def update_section(
    db: Session,
    tenant_id: int,
    section_id: int,
    data: SectionUpdate
) -> Optional[Section]:
    db_obj = get_section(db, tenant_id, section_id)
    if not db_obj:
        return None
    
    # If class is being updated, verify it exists
    if data.class_id:
        class_obj = get_class(db, tenant_id, data.class_id)
        if not class_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    
    db.commit()
    db.refresh(db_obj)
    
    # Invalidate cache
    cache.delete(f"section:{tenant_id}:{section_id}")
    
    return db_obj

# Student Section Assignment
def assign_student_to_section(
    db: Session,
    tenant_id: int,
    data: StudentSectionCreate
) -> StudentSection:
    # Verify section exists and belongs to tenant
    section = get_section(db, tenant_id, data.section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    # Check if student is already assigned to a section in this class
    existing_assignment = db.query(StudentSection).join(Section).filter(
        and_(
            StudentSection.tenant_id == tenant_id,
            StudentSection.student_id == data.student_id,
            Section.class_id == section.class_id
        )
    ).first()
    
    if existing_assignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already assigned to a section in this class"
        )
    
    # Check section capacity
    current_students = db.query(StudentSection).filter(
        and_(
            StudentSection.section_id == data.section_id,
            StudentSection.is_active == True
        )
    ).count()
    
    if current_students >= section.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Section capacity reached"
        )
    
    data_dict = data.model_dump()
    data_dict["tenant_id"] = tenant_id
    db_obj = StudentSection(**data_dict)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# Teacher Section Assignment
def assign_teacher_to_section(
    db: Session,
    tenant_id: int,
    data: TeacherSectionCreate
) -> TeacherSection:
    # Verify section exists and belongs to tenant
    section = get_section(db, tenant_id, data.section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    # If assigning as class teacher, check if section already has one
    if data.is_class_teacher:
        existing_class_teacher = db.query(TeacherSection).filter(
            and_(
                TeacherSection.section_id == data.section_id,
                TeacherSection.is_class_teacher == True
            )
        ).first()
        
        if existing_class_teacher:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Section already has a class teacher"
            )
    
    data_dict = data.model_dump()
    data_dict["tenant_id"] = tenant_id
    db_obj = TeacherSection(**data_dict)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# Utility functions
def get_class_students(
    db: Session,
    tenant_id: int,
    class_id: int,
    is_active: Optional[bool] = None
) -> List[Dict[str, Any]]:
    cache_key = f"class_students:{tenant_id}:{class_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    query = db.query(
        StudentSection.student_id,
        StudentSection.roll_number,
        Section.name.label("section_name"),
        StudentSection.is_active
    ).join(Section).filter(
        and_(
            StudentSection.tenant_id == tenant_id,
            Section.class_id == class_id
        )
    )
    
    if is_active is not None:
        query = query.filter(StudentSection.is_active == is_active)
    
    result = [
        {
            "student_id": row.student_id,
            "roll_number": row.roll_number,
            "section_name": row.section_name,
            "is_active": row.is_active
        }
        for row in query.all()
    ]
    
    cache.set(cache_key, result, ttl=300)  # Cache for 5 minutes
    
    return result

def get_teacher_classes(
    db: Session,
    tenant_id: int,
    teacher_id: int,
    academic_year_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    cache_key = f"teacher_classes:{tenant_id}:{teacher_id}:{academic_year_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    query = db.query(
        Class.id.label("class_id"),
        Class.name.label("class_name"),
        Section.id.label("section_id"),
        Section.name.label("section_name"),
        TeacherSection.is_class_teacher
    ).join(
        Section, Class.id == Section.class_id
    ).join(
        TeacherSection, Section.id == TeacherSection.section_id
    ).filter(
        and_(
            TeacherSection.tenant_id == tenant_id,
            TeacherSection.teacher_id == teacher_id
        )
    )
    
    if academic_year_id:
        query = query.filter(Class.academic_year_id == academic_year_id)
    
    result = [
        {
            "class_id": row.class_id,
            "class_name": row.class_name,
            "section_id": row.section_id,
            "section_name": row.section_name,
            "is_class_teacher": row.is_class_teacher
        }
        for row in query.all()
    ]
    
    cache.set(cache_key, result, ttl=300)  # Cache for 5 minutes
    
    return result

# Subject CRUD
def create_subject(db: Session, tenant_id: int, data: SubjectCreate) -> Subject:
    data_dict = data.model_dump()
    data_dict["tenant_id"] = tenant_id
    db_obj = Subject(**data_dict)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_subject(db: Session, tenant_id: Optional[int], subject_id: int) -> Optional[Subject]:
    cache_key = f"subject:{tenant_id}:{subject_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return Subject(**{k: v for k, v in cached_data.items() if not k.startswith('_')})
    
    query = db.query(Subject).filter(Subject.id == subject_id)
    if tenant_id is not None:
        query = query.filter(Subject.tenant_id == tenant_id)
    
    db_obj = query.first()
    
    if db_obj:
        # Convert SQLAlchemy model to dict, excluding private attributes
        obj_dict = {k: v for k, v in db_obj.__dict__.items() if not k.startswith('_')}
        cache.set(cache_key, obj_dict, ttl=3600)
    
    return db_obj

def get_subjects(
    db: Session,
    tenant_id: Optional[int],
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None
) -> List[Subject]:
    query = db.query(Subject)
    
    if tenant_id is not None:
        query = query.filter(Subject.tenant_id == tenant_id)
    
    if is_active is not None:
        query = query.filter(Subject.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()

def update_subject(
    db: Session,
    tenant_id: int,
    subject_id: int,
    data: SubjectUpdate
) -> Optional[Subject]:
    db_obj = get_subject(db, tenant_id, subject_id)
    if not db_obj:
        return None
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    
    db.commit()
    db.refresh(db_obj)
    
    # Invalidate cache
    cache.delete(f"subject:{tenant_id}:{subject_id}")
    
    return db_obj
