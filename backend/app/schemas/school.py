from pydantic import BaseModel
from app.schemas.base import TimestampSchema

class SchoolBase(BaseModel):
    name: str
    address: str | None = None
    phone: str | None = None

class SchoolCreate(SchoolBase):
    tenant_id: int

class SchoolUpdate(SchoolBase):
    pass

class SchoolInDB(SchoolBase, TimestampSchema):
    id: int
    tenant_id: int