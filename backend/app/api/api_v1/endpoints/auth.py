from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_user, require_school_admin
from app.schemas.auth import Token, RegisterUser, Login
from app.services.auth import authenticate_user, create_access_token, create_user
from app.services.saas_auth import authenticate_saas_admin, create_saas_access_token
from app.models.user import User
from app.models.saas import SaaSAdmin

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    login_data: Login,
    db: Session = Depends(get_db)
) -> Token:
    try:
        # First try SaaS admin authentication
        admin = authenticate_saas_admin(db, login_data.email, login_data.password)
        if admin:
            if not admin.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin account is inactive",
                )
            access_token = create_saas_access_token(admin)
            return Token(access_token=access_token, token_type="bearer")
        
        # If not a SaaS admin, try regular user authentication
        user = authenticate_user(db, login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Convert string "true" or "1" to boolean
        is_active = user.is_active.lower() in ("true", "1") if isinstance(user.is_active, str) else bool(user.is_active)
        print(f"Debug - is_active value: {user.is_active}, converted to: {is_active}")
        
        if not is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )
        
        access_token = create_access_token(user)
        return Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        print(f"Login error: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/register", response_model=None)
async def register(
    user_data: RegisterUser,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin)
) -> dict:
    """
    Register a new user (requires school_admin or higher role)
    """
    user = create_user(
        db,
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        role=user_data.role,
        tenant_id=user_data.tenant_id,
        created_by_role=current_user.role
    )
    
    return {"message": "User created successfully", "user_id": user.id}

@router.get("/me")
async def get_current_user_info(current_user: Union[User, SaaSAdmin] = Depends(get_current_user)) -> dict:
    """
    Get current user information
    """
    if isinstance(current_user, User):
        return {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "role": current_user.role,
            "is_active": current_user.is_active,
            "tenant_id": current_user.tenant_id,
            "is_saas_admin": False
        }
    else:
        return {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "role": current_user.role,
            "is_active": current_user.is_active,
            "is_saas_admin": True,
            "full_name": current_user.full_name,
            "phone": current_user.phone
        }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)) -> dict:
    """
    Logout endpoint (client should discard the token)
    """
    return {"message": "Successfully logged out"}