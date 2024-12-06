from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolUpdate
from app.services.tenant import get_tenant

def create_school(db: Session, school_data: SchoolCreate) -> School:
    # Verify tenant exists
    get_tenant(db, school_data.tenant_id)
    
    school = School(**school_data.model_dump())
    db.add(school)
    db.commit()
    db.refresh(school)
    return school

def get_school(db: Session, school_id: int) -> School:
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    return school

def get_schools(
    db: Session,
    tenant_id: int | None = None,
    skip: int = 0,
    limit: int = 100
) -> List[School]:
    query = db.query(School)
    if tenant_id:
        query = query.filter(School.tenant_id == tenant_id)
    return query.offset(skip).limit(limit).all()

def update_school(
    db: Session,
    school_id: int,
    school_data: SchoolUpdate
) -> School:
    school = get_school(db, school_id)
    for field, value in school_data.model_dump(exclude_unset=True).items():
        setattr(school, field, value)
    
    db.commit()
    db.refresh(school)
    return school

def delete_school(db: Session, school_id: int) -> None:
    school = get_school(db, school_id)
    db.delete(school)
    db.commit()