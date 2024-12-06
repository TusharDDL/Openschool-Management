from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate

def create_tenant(db: Session, tenant_data: TenantCreate) -> Tenant:
    tenant = Tenant(**tenant_data.model_dump())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

def get_tenant(db: Session, tenant_id: int) -> Tenant:
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    return tenant

def get_tenants(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Tenant]:
    return db.query(Tenant).offset(skip).limit(limit).all()

def update_tenant(
    db: Session,
    tenant_id: int,
    tenant_data: TenantUpdate
) -> Tenant:
    tenant = get_tenant(db, tenant_id)
    for field, value in tenant_data.model_dump(exclude_unset=True).items():
        setattr(tenant, field, value)
    
    db.commit()
    db.refresh(tenant)
    return tenant

def delete_tenant(db: Session, tenant_id: int) -> None:
    tenant = get_tenant(db, tenant_id)
    db.delete(tenant)
    db.commit()