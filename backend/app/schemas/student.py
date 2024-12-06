from typing import Optional, List
from datetime import date
from pydantic import BaseModel, EmailStr, validator, Field
from app.models.student import Gender, BloodGroup

# Base Schemas
class StudentProfileBase(BaseModel):
    admission_number: str
    admission_date: date
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    date_of_birth: date
    gender: Gender
    blood_group: Optional[BloodGroup] = None
    address: str = Field(..., min_length=5)
    phone: Optional[str] = None
    emergency_contact: str
    medical_conditions: Optional[str] = None
    previous_school: Optional[str] = None
    is_active: bool = True

    @validator('admission_date')
    def validate_admission_date(cls, v):
        if v > date.today():
            raise ValueError('Admission date cannot be in the future')
        return v

    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return v

    @validator('phone', 'emergency_contact')
    def validate_phone(cls, v):
        if v and not v.replace('+', '').isdigit():
            raise ValueError('Invalid phone number')
        return v

class GuardianBase(BaseModel):
    relationship: str = Field(..., min_length=2)
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    occupation: Optional[str] = None
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    is_emergency_contact: bool = False
    is_authorized_pickup: bool = False

    @validator('phone')
    def validate_phone(cls, v):
        if not v.replace('+', '').isdigit():
            raise ValueError('Invalid phone number')
        return v

class StudentDocumentBase(BaseModel):
    document_type: str
    file_name: str
    file_size: int
    mime_type: str
    is_verified: bool = False

    @validator('file_size')
    def validate_file_size(cls, v):
        max_size = 10 * 1024 * 1024  # 10MB
        if v > max_size:
            raise ValueError('File size too large')
        return v

class StudentNoteBase(BaseModel):
    note_type: str
    title: str = Field(..., min_length=3)
    content: str = Field(..., min_length=10)
    is_confidential: bool = False

# Create Schemas
class StudentProfileCreate(StudentProfileBase):
    guardians: List[GuardianBase]

class GuardianCreate(GuardianBase):
    pass

class StudentDocumentCreate(StudentDocumentBase):
    student_id: int

class StudentNoteCreate(StudentNoteBase):
    student_id: int

# Update Schemas
class StudentProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_conditions: Optional[str] = None
    is_active: Optional[bool] = None

    @validator('phone', 'emergency_contact')
    def validate_phone(cls, v):
        if v and not v.replace('+', '').isdigit():
            raise ValueError('Invalid phone number')
        return v

class GuardianUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    occupation: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    is_emergency_contact: Optional[bool] = None
    is_authorized_pickup: Optional[bool] = None

    @validator('phone')
    def validate_phone(cls, v):
        if v and not v.replace('+', '').isdigit():
            raise ValueError('Invalid phone number')
        return v

class StudentDocumentUpdate(BaseModel):
    is_verified: Optional[bool] = None
    verification_date: Optional[date] = None

class StudentNoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_confidential: Optional[bool] = None

# Response Schemas
class Guardian(GuardianBase):
    id: int
    student_id: int
    user_id: Optional[int]
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True

class StudentDocument(StudentDocumentBase):
    id: int
    student_id: int
    document_url: str
    uploaded_by: int
    verified_by: Optional[int]
    verification_date: Optional[date]
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True

class StudentNote(StudentNoteBase):
    id: int
    student_id: int
    created_by: int
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True

class StudentProfile(StudentProfileBase):
    id: int
    user_id: int
    tenant_id: int
    guardians: List[Guardian]
    documents: Optional[List[StudentDocument]] = None
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True

# Additional Response Schemas
class StudentAttendanceSummary(BaseModel):
    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    excused_days: int
    attendance_percentage: float

class StudentBasicInfo(BaseModel):
    id: int
    admission_number: str
    first_name: str
    last_name: str
    section_name: Optional[str]
    roll_number: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True

class StudentDetailedInfo(StudentProfile):
    attendance_summary: Optional[StudentAttendanceSummary]
    current_section: Optional[str]
    current_class: Optional[str]
    academic_year: Optional[str]

    class Config:
        orm_mode = True
