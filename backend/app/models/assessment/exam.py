from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Enum as SQLEnum, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ExamType(str, Enum):
    UNIT_TEST = "UNIT_TEST"
    MID_TERM = "MID_TERM"
    FINAL = "FINAL"
    PRACTICAL = "PRACTICAL"
    PROJECT = "PROJECT"
    ASSIGNMENT = "ASSIGNMENT"
    OTHER = "OTHER"

class GradeScale(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    GRADE_POINTS = "GRADE_POINTS"
    LETTER_GRADE = "LETTER_GRADE"
    PASS_FAIL = "PASS_FAIL"

class Exam(BaseModel):
    __tablename__ = "exams"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'academic_year_id', 'name', name='uq_exam_name'),
        {'schema': 'assessment'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic.academic_years.id", ondelete="CASCADE"), nullable=False)
    term_id = Column(Integer, ForeignKey("academic.terms.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    exam_type = Column(SQLEnum(ExamType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    grade_scale = Column(SQLEnum(GradeScale), nullable=False)
    passing_percentage = Column(Float, nullable=False)
    description = Column(Text)
    is_published = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    academic_year = relationship("AcademicYear")
    term = relationship("Term")
    exam_subjects = relationship("ExamSubject", back_populates="exam", cascade="all, delete-orphan")
    exam_results = relationship("ExamResult", back_populates="exam", cascade="all, delete-orphan")

class ExamSubject(BaseModel):
    __tablename__ = "exam_subjects"
    __table_args__ = (
        UniqueConstraint('exam_id', 'subject_id', name='uq_exam_subject'),
        {'schema': 'assessment'}
    )

    exam_id = Column(Integer, ForeignKey("assessment.exams.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("public.subjects.id", ondelete="CASCADE"), nullable=False)
    max_marks = Column(Float, nullable=False)
    passing_marks = Column(Float, nullable=False)
    exam_date = Column(Date, nullable=False)
    start_time = Column(String)  # Format: "HH:MM"
    duration = Column(Integer)  # in minutes
    instructions = Column(Text)
    is_practical = Column(Boolean, default=False)

    # Relationships
    exam = relationship("Exam", back_populates="exam_subjects")
    subject = relationship("Subject")
    exam_results = relationship("ExamResult", back_populates="exam_subject", cascade="all, delete-orphan")

class ExamResult(BaseModel):
    __tablename__ = "exam_results"
    __table_args__ = (
        UniqueConstraint('exam_id', 'exam_subject_id', 'student_id', name='uq_exam_result'),
        {'schema': 'assessment'}
    )

    exam_id = Column(Integer, ForeignKey("assessment.exams.id", ondelete="CASCADE"), nullable=False)
    exam_subject_id = Column(Integer, ForeignKey("assessment.exam_subjects.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("public.student_profiles.id", ondelete="CASCADE"), nullable=False)
    marks_obtained = Column(Float, nullable=False)
    grade = Column(String)  # For letter grades
    remarks = Column(Text)
    is_absent = Column(Boolean, default=False)
    is_exempted = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("public.users.id"))
    verification_date = Column(Date)

    # Relationships
    exam = relationship("Exam", back_populates="exam_results")
    exam_subject = relationship("ExamSubject", back_populates="exam_results")
    student = relationship("StudentProfile")
    verifier = relationship("User")

class GradeRule(BaseModel):
    __tablename__ = "grade_rules"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'academic_year_id', 'min_percentage', name='uq_grade_rule'),
        {'schema': 'assessment'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic.academic_years.id", ondelete="CASCADE"), nullable=False)
    grade = Column(String, nullable=False)  # A+, A, B+, etc.
    min_percentage = Column(Float, nullable=False)
    max_percentage = Column(Float, nullable=False)
    grade_point = Column(Float)  # For GPA calculation
    description = Column(Text)
    is_pass = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    academic_year = relationship("AcademicYear")