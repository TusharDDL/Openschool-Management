from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda dt: dt.isoformat() if dt else None},
        populate_by_name=True,
        json_schema_extra={"example": {"created_at": "2024-12-16T17:55:52.624382+00:00"}}
    )

class TimestampSchema(BaseSchema):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None