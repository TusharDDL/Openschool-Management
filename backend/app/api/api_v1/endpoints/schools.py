from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import require_school_admin, get_current_user
from app.models.user import User
from app.models.saas import SaaSAdmin
from app.schemas.school import SchoolCreate, SchoolUpdate, SchoolInDB
from app.services import school as school_service

router = APIRouter()

@router.post("", response_model=SchoolInDB, status_code=status.HTTP_201_CREATED)
async def create_school(
    school_data: SchoolCreate,
    db: Session = Depends(get_db),
    current_user: Union[User, SaaSAdmin] = Depends(require_school_admin)
) -> SchoolInDB:
    """
    Create a new school (School Admin or higher)
    """
    # SaaS admins can create schools in any tenant
    if not isinstance(current_user, SaaSAdmin):
        # Regular users can only create schools in their tenant
        if current_user.tenant_id != school_data.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create school for different tenant"
            )
    return school_service.create_school(db, school_data)

@router.get("", response_model=List[SchoolInDB])
async def list_schools(
    tenant_id: int | None = Query(None, description="Filter schools by tenant ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Union[User, SaaSAdmin] = Depends(get_current_user)
) -> List[SchoolInDB]:
    """
    List schools (filtered by tenant_id if provided)
    """
    # SaaS admins can see schools from any tenant
    if isinstance(current_user, SaaSAdmin):
        return school_service.get_schools(
            db, 
            tenant_id=tenant_id,
            skip=skip,
            limit=limit
        )
    
    # Regular users can only see schools in their tenant
    tenant_id = tenant_id or current_user.tenant_id
    if current_user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access schools from different tenant"
        )
    
    return school_service.get_schools(
        db, 
        tenant_id=tenant_id,
        skip=skip,
        limit=limit
    )

@router.get("/{school_id}", response_model=SchoolInDB)
async def get_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user: Union[User, SaaSAdmin] = Depends(get_current_user)
) -> SchoolInDB:
    """
    Get school by ID
    """
    school = school_service.get_school(db, school_id)
    
    # SaaS admins can see any school
    if not isinstance(current_user, SaaSAdmin):
        # Regular users can only see schools in their tenant
        if school.tenant_id != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access school from different tenant"
            )
    
    return school

@router.put("/{school_id}", response_model=SchoolInDB)
async def update_school(
    school_id: int,
    school_data: SchoolUpdate,
    db: Session = Depends(get_db),
    current_user: Union[User, SaaSAdmin] = Depends(require_school_admin)
) -> SchoolInDB:
    """
    Update school details (School Admin or higher)
    """
    school = school_service.get_school(db, school_id)
    
    # SaaS admins can update any school
    if not isinstance(current_user, SaaSAdmin):
        # Regular admins can only update schools in their tenant
        if school.tenant_id != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot update school from different tenant"
            )
    
    return school_service.update_school(db, school_id, school_data)

@router.delete("/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user: Union[User, SaaSAdmin] = Depends(require_school_admin)
) -> None:
    """
    Delete school (School Admin or higher)
    """
    school = school_service.get_school(db, school_id)
    
    # SaaS admins can delete any school
    if not isinstance(current_user, SaaSAdmin):
        # Regular admins can only delete schools in their tenant
        if school.tenant_id != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete school from different tenant"
            )
    
    school_service.delete_school(db, school_id)