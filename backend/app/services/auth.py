from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt

from app.core.config import get_settings
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.models.enums import UserRole, ROLE_HIERARCHY
from app.schemas.auth import TokenData

settings = get_settings()

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    try:
        print(f"Attempting to authenticate user: {email}")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print("User not found")
            return None
        
        print(f"Found user: {user.email}, role: {user.role}, is_active: {user.is_active}")
        if not verify_password(password, user.hashed_password):
            print("Invalid password")
            return None
            
        # Convert numeric is_active to boolean if needed
        if isinstance(user.is_active, int):
            user.is_active = bool(user.is_active)
            
        return user
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def create_access_token(user: User) -> str:
    try:
        token_data = TokenData(
            user_id=user.id,
            tenant_id=user.tenant_id,
            role=user.role
        )
        
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "exp": expire,
            "sub": str(token_data.user_id),
            "tenant_id": token_data.tenant_id,
            "role": token_data.role
        }
        
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating access token: {str(e)}"
        )

def create_user(
    db: Session,
    *,
    email: str,
    username: str,
    password: str,
    role: UserRole,
    tenant_id: int,
    created_by_role: UserRole
) -> User:
    try:
        # Check if the creating user has sufficient privileges
        if ROLE_HIERARCHY[created_by_role] <= ROLE_HIERARCHY[role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to create user with this role"
            )
        
        # Check if email already exists
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        if db.query(User).filter(User.username == username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            role=role,
            tenant_id=tenant_id,
            is_active=True  # Set as boolean
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

def check_permission(required_role: UserRole, user_role: UserRole) -> bool:
    return ROLE_HIERARCHY[user_role] >= ROLE_HIERARCHY[required_role]