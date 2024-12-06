from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate

def create_tenant(db: Session, data: TenantCreate) -> Tenant:
    db_obj = Tenant(**data.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_tenant(db: Session, tenant_id: int) -> Optional[Tenant]:
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()

def get_tenants(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None
) -> List[Tenant]:
    query = db.query(Tenant)
    if is_active is not None:
        query = query.filter(Tenant.is_active == is_active)
    return query.offset(skip).limit(limit).all()

def update_tenant(
    db: Session,
    tenant_id: int,
    data: TenantUpdate
) -> Optional[Tenant]:
    db_obj = get_tenant(db, tenant_id)
    if not db_obj:
        return None
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_tenant(db: Session, tenant_id: int) -> bool:
    db_obj = get_tenant(db, tenant_id)
    if not db_obj:
        return False
    
    db.delete(db_obj)
    db.commit()
    return True