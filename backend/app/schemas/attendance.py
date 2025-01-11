from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional, List, Dict
from app.schemas.base import TimestampSchema

class AttendanceBase(BaseModel):
    student_id: int
    date: date
    status: str = Field(..., description="present, absent, late, excused")
    remarks: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    class_id: int
    section_id: Optional[int] = None
    subject_id: Optional[int] = None
    time_in: Optional[time] = None
    time_out: Optional[time] = None

class AttendanceUpdate(BaseModel):
    status: Optional[str] = None
    remarks: Optional[str] = None
    time_in: Optional[time] = None
    time_out: Optional[time] = None

class AttendanceResponse(AttendanceBase, TimestampSchema):
    id: int
    class_id: int
    section_id: Optional[int]
    subject_id: Optional[int]
    marked_by: int
    time_in: Optional[time]
    time_out: Optional[time]

class StudentAttendanceSummary(BaseModel):
    student_id: int
    student_name: str
    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    excused_days: int
    attendance_percentage: float

class AttendanceReport(BaseModel):
    class_id: int
    class_name: str
    start_date: date
    end_date: date
    total_working_days: int
    student_summaries: List[StudentAttendanceSummary]
    daily_attendance: Dict[str, Dict[int, str]]  # date -> {student_id: status}