from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, check_rate_limit
from app.core.security import require_school_admin
from app.schemas.academic import Subject, SubjectCreate, SubjectUpdate
from app.crud import academic as crud_academic
from app.models.user import User

router = APIRouter()

@router.post("", response_model=Subject, status_code=status.HTTP_201_CREATED)
async def create_subject(
    data: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Create a new subject (requires school_admin role)"""
    return crud_academic.create_subject(db, current_user.tenant_id, data)

@router.get("", response_model=List[Subject])
async def list_subjects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """List subjects"""
    return crud_academic.get_subjects(
        db,
        current_user.tenant_id,
        skip=skip,
        limit=limit,
        is_active=is_active
    )

@router.get("/{subject_id}", response_model=Subject)
async def get_subject_by_id(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Get subject by ID"""
    db_obj = crud_academic.get_subject(db, current_user.tenant_id, subject_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return db_obj

@router.put("/{subject_id}", response_model=Subject)
async def update_subject(
    subject_id: int,
    data: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin),
    _: bool = Depends(check_rate_limit)
):
    """Update subject (requires school_admin role)"""
    db_obj = crud_academic.update_subject(
        db,
        current_user.tenant_id,
        subject_id,
        data
    )
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return db_obj