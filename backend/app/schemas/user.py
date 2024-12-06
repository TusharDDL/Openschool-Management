from pydantic import BaseModel, EmailStr
from app.schemas.base import TimestampSchema
from app.models.enums import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    tenant_id: int

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None

class UserInDB(UserBase, TimestampSchema):
    id: int
    tenant_id: int