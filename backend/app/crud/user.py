from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

def create_user(db: Session, data: UserCreate) -> User:
    db_obj = User(
        **data.model_dump(exclude={'password'}),
        hashed_password=get_password_hash(data.password)
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_user(db: Session, tenant_id: int, user_id: int) -> Optional[User]:
    return db.query(User).filter(
        User.id == user_id,
        User.tenant_id == tenant_id
    ).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_users(
    db: Session,
    tenant_id: int,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None
) -> List[User]:
    query = db.query(User).filter(User.tenant_id == tenant_id)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.offset(skip).limit(limit).all()

def update_user(
    db: Session,
    tenant_id: int,
    user_id: int,
    data: UserUpdate
) -> Optional[User]:
    db_obj = get_user(db, tenant_id, user_id)
    if not db_obj:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    if 'password' in update_data:
        update_data['hashed_password'] = get_password_hash(update_data.pop('password'))
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_user(db: Session, tenant_id: int, user_id: int) -> bool:
    db_obj = get_user(db, tenant_id, user_id)
    if not db_obj:
        return False
    
    db.delete(db_obj)
    db.commit()
    return True