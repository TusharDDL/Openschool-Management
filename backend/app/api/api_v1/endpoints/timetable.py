from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, check_rate_limit
from app.core.security import require_school_admin
from app.schemas.timetable import (
    Timetable, TimetableCreate, TimetableUpdate,
    TimetablePeriod, TimetablePeriodCreate, TimetablePeriodUpdate
)
from app.crud import timetable as crud_timetable
from app.models.user import User

router = APIRouter()

# Timetable routes
@router.post("/timetables", response_model=Timetable, status_code=status.HTTP_201_CREATED)
async def create_timetable(
    data: TimetableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Create a new timetable (requires school_admin role)"""
    return crud_timetable.create_timetable(db, current_user.tenant_id, data)

@router.get("/timetables", response_model=List[Timetable])
async def list_timetables(
    academic_year_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """List timetables"""
    return crud_timetable.get_timetables(
        db,
        current_user.tenant_id,
        academic_year_id=academic_year_id,
        skip=skip,
        limit=limit,
        is_active=is_active
    )

@router.get("/timetables/{timetable_id}", response_model=Timetable)
async def get_timetable_by_id(
    timetable_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Get timetable by ID"""
    db_obj = crud_timetable.get_timetable(db, current_user.tenant_id, timetable_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable not found"
        )
    return db_obj

@router.put("/timetables/{timetable_id}", response_model=Timetable)
async def update_timetable(
    timetable_id: int,
    data: TimetableUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Update timetable (requires school_admin role)"""
    db_obj = crud_timetable.update_timetable(
        db,
        current_user.tenant_id,
        timetable_id,
        data
    )
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable not found"
        )
    return db_obj

# Timetable Period routes
@router.post("/timetables/{timetable_id}/periods", response_model=TimetablePeriod, status_code=status.HTTP_201_CREATED)
async def create_period(
    timetable_id: int,
    data: TimetablePeriodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Create a new period in a timetable (requires school_admin role)"""
    if data.timetable_id != timetable_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Timetable ID mismatch"
        )
    return crud_timetable.create_period(db, current_user.tenant_id, data)

@router.get("/timetables/{timetable_id}/periods", response_model=List[TimetablePeriod])
async def list_periods(
    timetable_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """List periods in a timetable"""
    return crud_timetable.get_periods(
        db,
        current_user.tenant_id,
        timetable_id,
        skip=skip,
        limit=limit
    )

@router.get("/timetables/{timetable_id}/periods/{period_id}", response_model=TimetablePeriod)
async def get_period_by_id(
    timetable_id: int,
    period_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Get period by ID"""
    db_obj = crud_timetable.get_period(db, current_user.tenant_id, period_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found"
        )
    if db_obj.timetable_id != timetable_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found in this timetable"
        )
    return db_obj

@router.put("/timetables/{timetable_id}/periods/{period_id}", response_model=TimetablePeriod)
async def update_period(
    timetable_id: int,
    period_id: int,
    data: TimetablePeriodUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Update period (requires school_admin role)"""
    db_obj = crud_timetable.get_period(db, current_user.tenant_id, period_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found"
        )
    if db_obj.timetable_id != timetable_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found in this timetable"
        )
    
    updated_obj = crud_timetable.update_period(
        db,
        current_user.tenant_id,
        period_id,
        data
    )
    return updated_obj