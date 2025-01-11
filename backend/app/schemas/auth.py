from typing import Optional, Union
from pydantic import BaseModel, EmailStr
from app.models.enums import UserRole
from app.models.saas import SaaSRole

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int
    tenant_id: Optional[int] = None
    role: Union[UserRole, SaaSRole]
    is_saas_admin: bool = False

class Login(BaseModel):
    email: EmailStr
    password: str

class RegisterUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: UserRole
    tenant_id: int