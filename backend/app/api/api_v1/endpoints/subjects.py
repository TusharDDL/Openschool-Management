from typing import List, Optional
from datetime import datetime
import json
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, check_rate_limit
from app.schemas.academic import Subject, SubjectCreate, SubjectUpdate
from app.crud import academic as crud_academic
from app.models.user import User

router = APIRouter()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

@router.post("", response_model=Subject, status_code=status.HTTP_201_CREATED)
async def create_subject(
    data: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Create a new subject"""
    # If current user is a SaaS admin, use tenant_id from data
    tenant_id = getattr(current_user, 'tenant_id', None) or data.tenant_id
    db_obj = crud_academic.create_subject(db, tenant_id, data)
    return Subject.model_validate(db_obj)

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
    # If current user is a SaaS admin, use None as tenant_id to get all subjects
    tenant_id = getattr(current_user, 'tenant_id', None)
    db_objs = crud_academic.get_subjects(
        db,
        tenant_id,
        skip=skip,
        limit=limit,
        is_active=is_active
    )
    return [Subject.model_validate(obj) for obj in db_objs]

@router.get("/{subject_id}", response_model=Subject)
async def get_subject_by_id(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Get subject by ID"""
    tenant_id = getattr(current_user, 'tenant_id', None)
    db_obj = crud_academic.get_subject(db, tenant_id, subject_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return Subject.model_validate(db_obj)

@router.put("/{subject_id}", response_model=Subject)
async def update_subject(
    subject_id: int,
    data: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(check_rate_limit)
):
    """Update subject"""
    tenant_id = getattr(current_user, 'tenant_id', None)
    db_obj = crud_academic.update_subject(
        db,
        tenant_id,
        subject_id,
        data
    )
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return Subject.model_validate(db_obj)