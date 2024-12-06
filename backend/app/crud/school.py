from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolUpdate

def create_school(db: Session, data: SchoolCreate) -> School:
    db_obj = School(**data.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_school(db: Session, tenant_id: int, school_id: int) -> Optional[School]:
    return db.query(School).filter(
        School.id == school_id,
        School.tenant_id == tenant_id
    ).first()

def get_schools(
    db: Session,
    tenant_id: int,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None
) -> List[School]:
    query = db.query(School).filter(School.tenant_id == tenant_id)
    if is_active is not None:
        query = query.filter(School.is_active == is_active)
    return query.offset(skip).limit(limit).all()

def update_school(
    db: Session,
    tenant_id: int,
    school_id: int,
    data: SchoolUpdate
) -> Optional[School]:
    db_obj = get_school(db, tenant_id, school_id)
    if not db_obj:
        return None
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_school(db: Session, tenant_id: int, school_id: int) -> bool:
    db_obj = get_school(db, tenant_id, school_id)
    if not db_obj:
        return False
    
    db.delete(db_obj)
    db.commit()
    return True