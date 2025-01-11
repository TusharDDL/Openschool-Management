from pydantic import BaseModel, field_validator
from datetime import time, date
from typing import Optional
from app.models.enums import WeekDay
from app.schemas.base import TimestampSchema

class TimetableBase(BaseModel):
    name: str
    effective_from: date
    is_active: Optional[bool] = True

class TimetableCreate(TimetableBase):
    tenant_id: int
    school_id: int
    academic_year_id: int

class TimetableUpdate(TimetableBase):
    pass

class Timetable(TimetableBase, TimestampSchema):
    id: int
    school_id: int
    academic_year_id: int

class TimetablePeriodBase(BaseModel):
    period_number: int
    name: str
    start_time: time
    end_time: time
    day: WeekDay
    room: Optional[str] = None

    @field_validator('end_time')
    def end_time_must_be_after_start_time(cls, v, info):
        values = info.data
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class TimetablePeriodCreate(TimetablePeriodBase):
    tenant_id: int
    timetable_id: int

class TimetablePeriodUpdate(TimetablePeriodBase):
    pass

class TimetablePeriod(TimetablePeriodBase, TimestampSchema):
    id: int
    timetable_id: int