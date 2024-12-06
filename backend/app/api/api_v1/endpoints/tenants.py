from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import require_super_admin
from app.models.user import User
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantInDB
from app.services import tenant as tenant_service

router = APIRouter()

@router.post("", response_model=TenantInDB, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
) -> TenantInDB:
    """
    Create a new tenant (Super Admin only)
    """
    return tenant_service.create_tenant(db, tenant_data)

@router.get("", response_model=List[TenantInDB])
async def list_tenants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
) -> List[TenantInDB]:
    """
    List all tenants (Super Admin only)
    """
    return tenant_service.get_tenants(db, skip=skip, limit=limit)

@router.get("/{tenant_id}", response_model=TenantInDB)
async def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
) -> TenantInDB:
    """
    Get tenant by ID (Super Admin only)
    """
    return tenant_service.get_tenant(db, tenant_id)

@router.put("/{tenant_id}", response_model=TenantInDB)
async def update_tenant(
    tenant_id: int,
    tenant_data: TenantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
) -> TenantInDB:
    """
    Update tenant details (Super Admin only)
    """
    return tenant_service.update_tenant(db, tenant_id, tenant_data)

@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
) -> None:
    """
    Delete tenant (Super Admin only)
    """
    tenant_service.delete_tenant(db, tenant_id)