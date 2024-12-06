from app.schemas.auth import Token, TokenData, Login, RegisterUser
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantInDB
from app.schemas.school import SchoolCreate, SchoolUpdate, SchoolInDB
from app.schemas.user import UserCreate, UserUpdate, UserInDB

__all__ = [
    # Auth
    "Token", "TokenData", "Login", "RegisterUser",
    # Tenant
    "TenantCreate", "TenantUpdate", "TenantInDB",
    # School
    "SchoolCreate", "SchoolUpdate", "SchoolInDB",
    # User
    "UserCreate", "UserUpdate", "UserInDB"
]