from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
from app.models.attendance import AttendanceStatus
from app.models.assignment import SubmissionStatus
from app.models.fee import PaymentStatus

class AttendanceSummary(BaseModel):
    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    attendance_percentage: float
    recent_attendance: List[AttendanceStatus]

class AssignmentSummary(BaseModel):
    total_assignments: int
    completed_assignments: int
    pending_assignments: int
    overdue_assignments: int
    recent_assignments: List[dict]

class FeeSummary(BaseModel):
    total_fees: float
    paid_amount: float
    pending_amount: float
    overdue_amount: float
    next_due_date: Optional[date]
    payment_status: PaymentStatus

class AcademicSummary(BaseModel):
    current_average: float
    subjects_at_risk: List[str]
    top_subjects: List[str]
    recent_assessments: List[dict]

class StudentDashboard(BaseModel):
    student_id: int
    name: str
    class_name: str
    section_name: Optional[str]
    attendance: AttendanceSummary
    assignments: AssignmentSummary
    fees: FeeSummary
    academics: AcademicSummary

class AssignmentDetail(BaseModel):
    id: int
    title: str
    subject: str
    due_date: datetime
    status: SubmissionStatus
    score: Optional[int]
    max_score: int
    file_url: Optional[str]
    feedback: Optional[str]

class StudentAssignments(BaseModel):
    pending: List[AssignmentDetail]
    submitted: List[AssignmentDetail]
    graded: List[AssignmentDetail]

class ResultDetail(BaseModel):
    subject: str
    assessments: List[dict]
    total_percentage: float
    grade: str
    class_average: float
    rank: int