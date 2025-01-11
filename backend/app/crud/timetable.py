from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from app.models.academic_timetable import Timetable, TimetablePeriod
from app.schemas.timetable import (
    TimetableCreate, TimetableUpdate,
    TimetablePeriodCreate, TimetablePeriodUpdate
)
from app.core.cache import CacheService

cache = CacheService()

# Timetable CRUD
def create_timetable(db: Session, tenant_id: int, data: TimetableCreate) -> Timetable:
    data_dict = data.model_dump()
    data_dict["tenant_id"] = tenant_id
    db_obj = Timetable(**data_dict)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_timetable(db: Session, tenant_id: int, timetable_id: int) -> Optional[Timetable]:
    cache_key = f"timetable:{tenant_id}:{timetable_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return Timetable(**cached_data)
    
    db_obj = db.query(Timetable).filter(
        and_(
            Timetable.tenant_id == tenant_id,
            Timetable.id == timetable_id
        )
    ).first()
    
    if db_obj:
        cache.set(cache_key, db_obj.__dict__, ttl=3600)
    
    return db_obj

def get_timetables(
    db: Session,
    tenant_id: int,
    academic_year_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None
) -> List[Timetable]:
    query = db.query(Timetable).filter(Timetable.tenant_id == tenant_id)
    
    if academic_year_id:
        query = query.filter(Timetable.academic_year_id == academic_year_id)
    
    if is_active is not None:
        query = query.filter(Timetable.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()

def update_timetable(
    db: Session,
    tenant_id: int,
    timetable_id: int,
    data: TimetableUpdate
) -> Optional[Timetable]:
    db_obj = get_timetable(db, tenant_id, timetable_id)
    if not db_obj:
        return None
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    
    db.commit()
    db.refresh(db_obj)
    
    # Invalidate cache
    cache.delete(f"timetable:{tenant_id}:{timetable_id}")
    
    return db_obj

# Timetable Period CRUD
def create_period(
    db: Session,
    tenant_id: int,
    data: TimetablePeriodCreate
) -> TimetablePeriod:
    # Verify timetable exists and belongs to tenant
    timetable = get_timetable(db, tenant_id, data.timetable_id)
    if not timetable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable not found"
        )
    
    # Check for overlapping periods
    existing_period = db.query(TimetablePeriod).filter(
        and_(
            TimetablePeriod.timetable_id == data.timetable_id,
            TimetablePeriod.day == data.day,
            TimetablePeriod.start_time <= data.end_time,
            TimetablePeriod.end_time >= data.start_time
        )
    ).first()
    
    if existing_period:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Period overlaps with existing period"
        )
    
    data_dict = data.model_dump()
    data_dict["tenant_id"] = tenant_id
    db_obj = TimetablePeriod(**data_dict)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_period(
    db: Session,
    tenant_id: int,
    period_id: int
) -> Optional[TimetablePeriod]:
    cache_key = f"period:{tenant_id}:{period_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return TimetablePeriod(**cached_data)
    
    db_obj = db.query(TimetablePeriod).filter(
        and_(
            TimetablePeriod.tenant_id == tenant_id,
            TimetablePeriod.id == period_id
        )
    ).first()
    
    if db_obj:
        cache.set(cache_key, db_obj.__dict__, ttl=3600)
    
    return db_obj

def get_periods(
    db: Session,
    tenant_id: int,
    timetable_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[TimetablePeriod]:
    return db.query(TimetablePeriod).filter(
        and_(
            TimetablePeriod.tenant_id == tenant_id,
            TimetablePeriod.timetable_id == timetable_id
        )
    ).offset(skip).limit(limit).all()

def update_period(
    db: Session,
    tenant_id: int,
    period_id: int,
    data: TimetablePeriodUpdate
) -> Optional[TimetablePeriod]:
    db_obj = get_period(db, tenant_id, period_id)
    if not db_obj:
        return None
    
    # Check for overlapping periods if time is being updated
    if data.start_time or data.end_time:
        start_time = data.start_time or db_obj.start_time
        end_time = data.end_time or db_obj.end_time
        day = data.day or db_obj.day
        
        existing_period = db.query(TimetablePeriod).filter(
            and_(
                TimetablePeriod.timetable_id == db_obj.timetable_id,
                TimetablePeriod.id != period_id,
                TimetablePeriod.day == day,
                TimetablePeriod.start_time <= end_time,
                TimetablePeriod.end_time >= start_time
            )
        ).first()
        
        if existing_period:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Period overlaps with existing period"
            )
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    
    db.commit()
    db.refresh(db_obj)
    
    # Invalidate cache
    cache.delete(f"period:{tenant_id}:{period_id}")
    
    return db_obj