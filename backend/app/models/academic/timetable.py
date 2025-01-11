from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, UniqueConstraint, Time, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class WeekDay(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

class Timetable(BaseModel):
    __tablename__ = "timetables"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'academic_year_id', 'name', name='uq_timetable_name'),
        {'schema': 'academic'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic.academic_years.id", ondelete="CASCADE"), nullable=False)
    term_id = Column(Integer, ForeignKey("academic.terms.id", ondelete="CASCADE"))
    
    name = Column(String, nullable=False)
    description = Column(Text)
    effective_from = Column(Date, nullable=False)
    effective_till = Column(Date)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    academic_year = relationship("AcademicYear")
    term = relationship("Term")
    periods = relationship("TimetablePeriod", back_populates="timetable", cascade="all, delete-orphan")
    schedules = relationship("ClassSchedule", back_populates="timetable", cascade="all, delete-orphan")

class TimetablePeriod(BaseModel):
    __tablename__ = "timetable_periods"
    __table_args__ = (
        UniqueConstraint('timetable_id', 'period_number', name='uq_period_number'),
        CheckConstraint('end_time > start_time', name='check_period_time'),
        {'schema': 'academic'}
    )

    timetable_id = Column(Integer, ForeignKey("academic.timetables.id", ondelete="CASCADE"), nullable=False)
    
    period_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)  # e.g., "First Period", "Break", "Lunch"
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_break = Column(Boolean, default=False)
    description = Column(Text)

    # Relationships
    timetable = relationship("Timetable", back_populates="periods")
    schedules = relationship("ClassSchedule", back_populates="period")

class ClassSchedule(BaseModel):
    __tablename__ = "class_schedules"
    __table_args__ = (
        UniqueConstraint(
            'timetable_id', 'section_id', 'period_id', 'weekday',
            name='uq_class_schedule'
        ),
        {'schema': 'academic'}
    )

    timetable_id = Column(Integer, ForeignKey("academic.timetables.id", ondelete="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey("academic.sections.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("academic.subjects.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    period_id = Column(Integer, ForeignKey("academic.timetable_periods.id", ondelete="CASCADE"), nullable=False)
    
    weekday = Column(SQLEnum(WeekDay), nullable=False)
    room_number = Column(String)
    is_substitute = Column(Boolean, default=False)
    substitute_note = Column(Text)
    is_cancelled = Column(Boolean, default=False)
    cancellation_reason = Column(Text)

    # Relationships
    timetable = relationship("Timetable", back_populates="schedules")
    section = relationship("Section")
    subject = relationship("Subject")
    teacher = relationship("User")
    period = relationship("TimetablePeriod", back_populates="schedules")

class TeacherAvailability(BaseModel):
    __tablename__ = "teacher_availabilities"
    __table_args__ = (
        UniqueConstraint(
            'teacher_id', 'weekday', 'start_time', 'end_time',
            name='uq_teacher_availability'
        ),
        CheckConstraint('end_time > start_time', name='check_availability_time'),
        {'schema': 'academic'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    weekday = Column(SQLEnum(WeekDay), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True)
    reason = Column(Text)
    is_recurring = Column(Boolean, default=True)
    effective_from = Column(Date)
    effective_till = Column(Date)

    # Relationships
    tenant = relationship("Tenant")
    teacher = relationship("User")

class SubstituteHistory(BaseModel):
    __tablename__ = "substitute_history"
    __table_args__ = {'schema': 'academic'}

    schedule_id = Column(Integer, ForeignKey("academic.class_schedules.id", ondelete="CASCADE"), nullable=False)
    original_teacher_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    substitute_teacher_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    assigned_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    date = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    notes = Column(Text)
    is_accepted = Column(Boolean)
    response_time = Column(DateTime)
    response_note = Column(Text)

    # Relationships
    schedule = relationship("ClassSchedule")
    original_teacher = relationship("User", foreign_keys=[original_teacher_id])
    substitute_teacher = relationship("User", foreign_keys=[substitute_teacher_id])
    assigned_by = relationship("User", foreign_keys=[assigned_by_id])