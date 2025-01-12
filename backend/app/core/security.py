from typing import Optional, Callable
from datetime import datetime, timedelta, UTC
from typing import Optional, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.config import get_settings
from app.api.deps import get_db
from app.models.user import User
from app.models.enums import UserRole, ROLE_HIERARCHY
from app.models.saas import SaaSAdmin, SaaSRole
from app.models.student import Guardian
from sqlalchemy import and_
# Role hierarchy for SaaS roles
SAAS_ROLE_HIERARCHY = {
    SaaSRole.SUPER_ADMIN: 100,
    SaaSRole.ADMIN: 90,
    SaaSRole.IMPLEMENTATION: 80,
    SaaSRole.SUPPORT: 70,
}

def check_permission(required_role: UserRole, user_role: UserRole) -> bool:
    return ROLE_HIERARCHY[user_role] >= ROLE_HIERARCHY[required_role]

async def verify_parent_child_relationship(
    db: Session,
    parent_user_id: int,
    student_id: int
) -> bool:
    """Verify that a parent has access to a student's data"""
    guardian = db.query(Guardian).filter(
        and_(
            Guardian.user_id == parent_user_id,
            Guardian.student_id == student_id
        )
    ).first()
    return guardian is not None

def check_saas_permission(required_role: SaaSRole, user_role: str | SaaSRole) -> bool:
    # Convert string role to enum if needed
    if isinstance(user_role, str):
        user_role = SaaSRole(user_role)
    return SAAS_ROLE_HIERARCHY[user_role] >= SAAS_ROLE_HIERARCHY[required_role]

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def create_access_token(
    subject: str,
    role: Optional[str] = None,
    tenant_id: Optional[int] = None,
    email: Optional[str] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "role": role,
        "tenant_id": tenant_id,
        "email": email
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User | SaaSAdmin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        is_saas_admin: bool = payload.get("is_saas_admin", False)
        if user_id is None:
            raise credentials_exception
            
        print(f"Token payload: {payload}")  # Debug log
    except JWTError as e:
        print(f"JWT decode error: {str(e)}")  # Debug log
        raise credentials_exception
    
    # Try to find user in the appropriate table
    if is_saas_admin:
        print(f"Looking up SaaS admin with ID: {user_id}")  # Debug log
        admin = db.query(SaaSAdmin).filter(SaaSAdmin.id == int(user_id)).first()
        if admin is not None:
            # Convert SQLAlchemy Column values to Python types
            admin_is_active = bool(str(admin.is_active).lower() in ('true', '1'))
            if not admin_is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Inactive admin"
                )
            print(f"Found SaaS admin: {admin.email}, role: {admin.role}")  # Debug log
            return admin
            
        print("SaaS admin not found, checking regular users...")  # Debug log
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None or str(user.role) != 'SUPER_ADMIN':
            raise credentials_exception
            
        # Convert SQLAlchemy Column values to Python types
        user_is_active = bool(str(user.is_active).lower() in ('true', '1'))
        if not user_is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        print(f"Found super admin user: {user.email}, role: {user.role}")  # Debug log
        return user
    else:
        print(f"Looking up regular user with ID: {user_id}")  # Debug log
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            print("User not found in database")  # Debug log
            raise credentials_exception
            
        # Convert SQLAlchemy Column values to Python types
        user_is_active = bool(str(user.is_active).lower() in ('true', '1'))
        if not user_is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        print(f"Found regular user: {user.email}, role: {user.role}")  # Debug log
        
        # Add token role and tenant_id from payload
        user.token_role = payload.get('role')
        user.token_tenant_id = payload.get('tenant_id')
        print(f"Added token data - role: {user.token_role}, tenant_id: {user.token_tenant_id}")
        
        return user

def require_role(required_role: UserRole) -> Callable:
    async def role_checker(
        current_user: User | SaaSAdmin = Depends(get_current_user)
    ) -> User | SaaSAdmin:
        if isinstance(current_user, SaaSAdmin):
            # SaaS admins have access to everything
            # Add tenant_id property to SaaS admin for compatibility
            current_user.tenant_id = None
            return current_user
        if not check_permission(required_role, current_user.role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {required_role} or higher required"
            )
        return current_user
    return role_checker

def require_saas_role(required_role: SaaSRole) -> Callable:
    async def role_checker(
        current_user: User | SaaSAdmin = Depends(get_current_user)
    ) -> SaaSAdmin:
        if not isinstance(current_user, SaaSAdmin):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="SaaS admin role required"
            )
        if not check_saas_permission(required_role, current_user.role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"SaaS role {required_role} or higher required"
            )
        return current_user
    return role_checker

# Convenience dependencies for common role checks
require_super_admin = require_role(UserRole.SUPER_ADMIN)
require_school_admin = require_role(UserRole.SCHOOL_ADMIN)
require_teacher = require_role(UserRole.TEACHER)
require_student = require_role(UserRole.STUDENT)
require_parent = require_role(UserRole.PARENT)

# SaaS role dependencies
require_saas_super_admin = require_saas_role(SaaSRole.SUPER_ADMIN)
require_saas_admin = require_saas_role(SaaSRole.ADMIN)
require_saas_implementation = require_saas_role(SaaSRole.IMPLEMENTATION)
require_saas_support = require_saas_role(SaaSRole.SUPPORT)
