from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, UniqueConstraint, JSON, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class SyllabusStatus(str, Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class TopicStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    DELAYED = "DELAYED"
    SKIPPED = "SKIPPED"

class Syllabus(BaseModel):
    __tablename__ = "syllabi"
    __table_args__ = (
        UniqueConstraint(
            'tenant_id', 'academic_year_id', 'subject_id', 'grade_level',
            name='uq_syllabus'
        ),
        {'schema': 'academic'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic.academic_years.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("academic.subjects.id", ondelete="CASCADE"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    approved_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="SET NULL"))
    
    name = Column(String, nullable=False)
    grade_level = Column(Integer, nullable=False)
    description = Column(Text)
    objectives = Column(Text)
    prerequisites = Column(Text)
    resources = Column(Text)
    teaching_methodology = Column(Text)
    assessment_criteria = Column(Text)
    status = Column(SQLEnum(SyllabusStatus), nullable=False, default=SyllabusStatus.DRAFT)
    version = Column(String)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON)  # For additional configurable fields

    # Relationships
    tenant = relationship("Tenant")
    academic_year = relationship("AcademicYear")
    subject = relationship("Subject")
    created_by = relationship("User", foreign_keys=[created_by_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])
    units = relationship("SyllabusUnit", back_populates="syllabus", cascade="all, delete-orphan")
    progress_records = relationship("SyllabusProgress", back_populates="syllabus", cascade="all, delete-orphan")

class SyllabusUnit(BaseModel):
    __tablename__ = "syllabus_units"
    __table_args__ = (
        UniqueConstraint('syllabus_id', 'unit_number', name='uq_unit_number'),
        {'schema': 'academic'}
    )

    syllabus_id = Column(Integer, ForeignKey("academic.syllabi.id", ondelete="CASCADE"), nullable=False)
    
    unit_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    objectives = Column(Text)
    duration_hours = Column(Float)  # Estimated teaching hours
    resources = Column(Text)
    teaching_points = Column(Text)
    assessment_strategy = Column(Text)
    order = Column(Integer, nullable=False)
    is_optional = Column(Boolean, default=False)

    # Relationships
    syllabus = relationship("Syllabus", back_populates="units")
    topics = relationship("SyllabusTopic", back_populates="unit", cascade="all, delete-orphan")

class SyllabusTopic(BaseModel):
    __tablename__ = "syllabus_topics"
    __table_args__ = (
        UniqueConstraint('unit_id', 'topic_number', name='uq_topic_number'),
        {'schema': 'academic'}
    )

    unit_id = Column(Integer, ForeignKey("academic.syllabus_units.id", ondelete="CASCADE"), nullable=False)
    
    topic_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    learning_objectives = Column(Text)
    teaching_methods = Column(Text)
    resources = Column(Text)
    activities = Column(Text)
    assessment = Column(Text)
    duration_hours = Column(Float)  # Estimated teaching hours
    order = Column(Integer, nullable=False)
    is_optional = Column(Boolean, default=False)
    prerequisites = Column(Text)
    key_points = Column(Text)

    # Relationships
    unit = relationship("SyllabusUnit", back_populates="topics")
    subtopics = relationship("SyllabusSubtopic", back_populates="topic", cascade="all, delete-orphan")
    progress_records = relationship("TopicProgress", back_populates="topic", cascade="all, delete-orphan")

class SyllabusSubtopic(BaseModel):
    __tablename__ = "syllabus_subtopics"
    __table_args__ = (
        UniqueConstraint('topic_id', 'subtopic_number', name='uq_subtopic_number'),
        {'schema': 'academic'}
    )

    topic_id = Column(Integer, ForeignKey("academic.syllabus_topics.id", ondelete="CASCADE"), nullable=False)
    
    subtopic_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    learning_points = Column(Text)
    activities = Column(Text)
    duration_hours = Column(Float)  # Estimated teaching hours
    order = Column(Integer, nullable=False)
    is_optional = Column(Boolean, default=False)

    # Relationships
    topic = relationship("SyllabusTopic", back_populates="subtopics")

class SyllabusProgress(BaseModel):
    __tablename__ = "syllabus_progress"
    __table_args__ = (
        UniqueConstraint('syllabus_id', 'section_id', name='uq_syllabus_progress'),
        {'schema': 'academic'}
    )

    syllabus_id = Column(Integer, ForeignKey("academic.syllabi.id", ondelete="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey("academic.sections.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    completion_percentage = Column(Float, default=0)
    last_updated = Column(DateTime)
    remarks = Column(Text)

    # Relationships
    syllabus = relationship("Syllabus", back_populates="progress_records")
    section = relationship("Section")
    teacher = relationship("User")

class TopicProgress(BaseModel):
    __tablename__ = "topic_progress"
    __table_args__ = (
        UniqueConstraint('topic_id', 'section_id', name='uq_topic_progress'),
        {'schema': 'academic'}
    )

    topic_id = Column(Integer, ForeignKey("academic.syllabus_topics.id", ondelete="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey("academic.sections.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    status = Column(SQLEnum(TopicStatus), nullable=False, default=TopicStatus.PENDING)
    start_date = Column(Date)
    completion_date = Column(Date)
    teaching_notes = Column(Text)
    challenges_faced = Column(Text)
    student_response = Column(Text)
    resources_used = Column(Text)
    assessment_notes = Column(Text)

    # Relationships
    topic = relationship("SyllabusTopic", back_populates="progress_records")
    section = relationship("Section")
    teacher = relationship("User")