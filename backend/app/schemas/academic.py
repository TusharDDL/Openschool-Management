from pydantic import BaseModel, Field, validator, ConfigDict
from datetime import time, date, datetime
from typing import Optional, List, Dict, Union
from app.models.academic_core import Subject, AcademicYear, Class, Section, StudentSection, TeacherSection
from app.models.enums import WeekDay, GradingSystem, AssessmentType
from app.schemas.base import TimestampSchema

class AcademicYearBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    is_active: Optional[bool] = True

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

class AcademicYearCreate(AcademicYearBase):
    tenant_id: int
    school_id: int

class AcademicYearUpdate(AcademicYearBase):
    pass

class AcademicYear(AcademicYearBase, TimestampSchema):
    id: int
    school_id: int

class ClassBase(BaseModel):
    academic_year_id: int
    name: str
    grade_level: int
    is_active: Optional[bool] = True

class ClassCreate(ClassBase):
    tenant_id: int
    school_id: int

class ClassUpdate(ClassBase):
    pass

class Class(ClassBase, TimestampSchema):
    id: int
    school_id: int

class SectionBase(BaseModel):
    class_id: int
    name: str
    capacity: int
    is_active: Optional[bool] = True

class SectionCreate(SectionBase):
    tenant_id: int

class SectionUpdate(SectionBase):
    pass

class Section(SectionBase, TimestampSchema):
    id: int

class SubjectBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    credits: Optional[float] = None
    is_active: Optional[bool] = True

class SubjectCreate(SubjectBase):
    tenant_id: int
    school_id: int

class SubjectUpdate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: int
    school_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def model_validate(cls, obj):
        if isinstance(obj, dict):
            return cls(**obj)
        return cls(
            id=obj.id,
            name=obj.name,
            code=obj.code,
            description=obj.description,
            credits=obj.credits,
            is_active=obj.is_active,
            school_id=obj.school_id,
            created_at=obj.created_at.isoformat() if obj.created_at else None,
            updated_at=obj.updated_at.isoformat() if obj.updated_at else None
        )

    def model_dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "credits": self.credits,
            "is_active": self.is_active,
            "school_id": self.school_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def dict(self):
        return self.model_dump()

    def json(self):
        return json.dumps(self.dict())

class StudentSectionBase(BaseModel):
    student_id: int
    section_id: int
    roll_number: Optional[str] = None

class StudentSectionCreate(StudentSectionBase):
    tenant_id: int

class StudentSection(StudentSectionBase, TimestampSchema):
    id: int

class TeacherSectionBase(BaseModel):
    teacher_id: int
    section_id: int
    subject_id: int
    is_class_teacher: bool = False

class TeacherSectionCreate(TeacherSectionBase):
    tenant_id: int

class TeacherSection(TeacherSectionBase, TimestampSchema):
    id: int

class TimetableBase(BaseModel):
    class_id: int
    section_id: Optional[int] = None
    subject_id: int
    teacher_id: int
    day: WeekDay
    start_time: time
    end_time: time
    room: Optional[str] = None

    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class TimetableCreate(TimetableBase):
    school_id: int

class TimetableUpdate(TimetableBase):
    is_active: Optional[bool] = None

class TimetableInDB(TimetableBase, TimestampSchema):
    id: int
    school_id: int
    is_active: bool

class GradingSystemBase(BaseModel):
    name: str
    type: GradingSystem
    scale: Dict[str, Union[float, str]]  # Example: {"A": 90, "B": 80} or {"4.0": "Excellent"}
    passing_grade: float

class GradingSystemCreate(GradingSystemBase):
    school_id: int

class GradingSystemUpdate(GradingSystemBase):
    pass

class GradingSystemInDB(GradingSystemBase, TimestampSchema):
    id: int
    school_id: int

class AssessmentBase(BaseModel):
    class_id: int
    section_id: Optional[int] = None
    subject_id: int
    teacher_id: int
    grading_system_id: int
    name: str
    type: AssessmentType
    total_marks: float = Field(gt=0)
    weightage: float = Field(gt=0, le=100)
    description: Optional[str] = None

class AssessmentCreate(AssessmentBase):
    school_id: int

class AssessmentUpdate(AssessmentBase):
    pass

class AssessmentInDB(AssessmentBase, TimestampSchema):
    id: int
    school_id: int

class ResultBase(BaseModel):
    marks_obtained: float
    remarks: Optional[str] = None

    @validator('marks_obtained')
    def validate_marks(cls, v, values):
        if v < 0:
            raise ValueError('marks_obtained cannot be negative')
        return v

class ResultCreate(ResultBase):
    assessment_id: int
    student_id: int

class ResultUpdate(ResultBase):
    pass

class ResultInDB(ResultBase, TimestampSchema):
    id: int
    assessment_id: int
    student_id: int

class TeacherNoteBase(BaseModel):
    class_id: int
    section_id: Optional[int] = None
    subject_id: int
    title: str
    content: str
    file_url: Optional[str] = None

class TeacherNoteCreate(TeacherNoteBase):
    school_id: int
    teacher_id: int

class TeacherNoteUpdate(TeacherNoteBase):
    pass

class TeacherNoteInDB(TeacherNoteBase, TimestampSchema):
    id: int
    school_id: int
    teacher_id: int

class StudentResult(BaseModel):
    student_id: int
    assessment_results: List[ResultInDB]
    total_percentage: float
    grade: str
    remarks: Optional[str] = None