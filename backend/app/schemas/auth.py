from pydantic import BaseModel, EmailStr
from app.models.enums import UserRole

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int
    tenant_id: int
    role: UserRole

class Login(BaseModel):
    email: EmailStr
    password: str

class RegisterUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: UserRole
    tenant_id: int