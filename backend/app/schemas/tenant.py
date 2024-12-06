from pydantic import BaseModel
from app.schemas.base import TimestampSchema

class TenantBase(BaseModel):
    name: str

class TenantCreate(TenantBase):
    pass

class TenantUpdate(TenantBase):
    pass

class TenantInDB(TenantBase, TimestampSchema):
    id: int