from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt

from app.core.config import get_settings
from app.core.security import get_password_hash, verify_password
from app.models.saas import SaaSAdmin, SaaSRole
from app.schemas.auth import TokenData

settings = get_settings()

def authenticate_saas_admin(db: Session, email: str, password: str) -> Optional[SaaSAdmin]:
    try:
        print(f"Attempting to authenticate SaaS admin: {email}")
        admin = db.query(SaaSAdmin).filter(SaaSAdmin.email == email).first()
        if not admin:
            print("Admin not found")
            return None
        
        print(f"Found admin: {admin.email}, role: {admin.role}, is_active: {admin.is_active}")
        if not verify_password(password, admin.hashed_password):
            print("Invalid password")
            return None
            
        return admin
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def create_saas_access_token(admin: SaaSAdmin) -> str:
    try:
        token_data = TokenData(
            user_id=admin.id,
            role=admin.role,
            is_saas_admin=True
        )
        
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "exp": expire,
            "sub": str(token_data.user_id),
            "role": token_data.role,
            "is_saas_admin": True
        }
        
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating access token: {str(e)}"
        )

def create_saas_admin(
    db: Session,
    *,
    email: str,
    username: str,
    password: str,
    role: SaaSRole,
    full_name: str,
    phone: Optional[str] = None,
    created_by_role: Optional[SaaSRole] = None
) -> SaaSAdmin:
    try:
        # Check if the creating admin has sufficient privileges
        if created_by_role and created_by_role != SaaSRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only super admins can create other admins"
            )
        
        # Check if email already exists
        if db.query(SaaSAdmin).filter(SaaSAdmin.email == email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        if db.query(SaaSAdmin).filter(SaaSAdmin.username == username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        admin = SaaSAdmin(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            role=role,
            full_name=full_name,
            phone=phone,
            is_active=True
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        return admin
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating admin: {str(e)}"
        )