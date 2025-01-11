from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, UniqueConstraint, JSON, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class AssignmentType(str, Enum):
    HOMEWORK = "HOMEWORK"
    PROJECT = "PROJECT"
    PRESENTATION = "PRESENTATION"
    RESEARCH = "RESEARCH"
    PRACTICAL = "PRACTICAL"
    GROUP_WORK = "GROUP_WORK"
    QUIZ = "QUIZ"
    OTHER = "OTHER"

class AssignmentStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    GRADING = "GRADING"
    GRADED = "GRADED"
    ARCHIVED = "ARCHIVED"

class SubmissionStatus(str, Enum):
    NOT_SUBMITTED = "NOT_SUBMITTED"
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    LATE_SUBMITTED = "LATE_SUBMITTED"
    RESUBMITTED = "RESUBMITTED"
    GRADED = "GRADED"
    RETURNED = "RETURNED"

class Assignment(BaseModel):
    __tablename__ = "assignments"
    __table_args__ = {'schema': 'academic'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("academic.subjects.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("academic.syllabus_topics.id", ondelete="SET NULL"))
    
    title = Column(String, nullable=False)
    description = Column(Text)
    assignment_type = Column(SQLEnum(AssignmentType), nullable=False)
    instructions = Column(Text)
    resources = Column(Text)  # Links or references
    attachments = Column(JSON)  # Array of file URLs
    max_score = Column(Float)
    passing_score = Column(Float)
    start_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    late_submission_deadline = Column(DateTime)
    late_submission_penalty = Column(Float)  # Percentage deduction
    estimated_time = Column(Integer)  # In minutes
    difficulty_level = Column(String)  # Easy, Medium, Hard
    is_group_work = Column(Boolean, default=False)
    max_group_size = Column(Integer)
    status = Column(SQLEnum(AssignmentStatus), nullable=False, default=AssignmentStatus.DRAFT)
    grading_criteria = Column(Text)
    allow_resubmission = Column(Boolean, default=False)
    resubmission_deadline = Column(DateTime)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    subject = relationship("Subject")
    teacher = relationship("User")
    topic = relationship("SyllabusTopic")
    section_assignments = relationship("SectionAssignment", back_populates="assignment", cascade="all, delete-orphan")
    rubrics = relationship("AssignmentRubric", back_populates="assignment", cascade="all, delete-orphan")

class SectionAssignment(BaseModel):
    __tablename__ = "section_assignments"
    __table_args__ = (
        UniqueConstraint('assignment_id', 'section_id', name='uq_section_assignment'),
        {'schema': 'academic'}
    )

    assignment_id = Column(Integer, ForeignKey("academic.assignments.id", ondelete="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey("academic.sections.id", ondelete="CASCADE"), nullable=False)
    
    custom_instructions = Column(Text)
    custom_due_date = Column(DateTime)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime)

    # Relationships
    assignment = relationship("Assignment", back_populates="section_assignments")
    section = relationship("Section")
    submissions = relationship("AssignmentSubmission", back_populates="section_assignment", cascade="all, delete-orphan")

class AssignmentRubric(BaseModel):
    __tablename__ = "assignment_rubrics"
    __table_args__ = {'schema': 'academic'}

    assignment_id = Column(Integer, ForeignKey("academic.assignments.id", ondelete="CASCADE"), nullable=False)
    
    criteria = Column(String, nullable=False)
    description = Column(Text)
    max_score = Column(Float, nullable=False)
    weight = Column(Float, default=1.0)
    order = Column(Integer, nullable=False)

    # Relationships
    assignment = relationship("Assignment", back_populates="rubrics")

class AssignmentSubmission(BaseModel):
    __tablename__ = "assignment_submissions"
    __table_args__ = (
        UniqueConstraint(
            'section_assignment_id', 'student_id', 'submission_number',
            name='uq_student_submission'
        ),
        {'schema': 'academic'}
    )

    section_assignment_id = Column(Integer, ForeignKey("academic.section_assignments.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("public.student_profiles.id", ondelete="CASCADE"), nullable=False)
    group_id = Column(Integer, ForeignKey("academic.assignment_groups.id", ondelete="SET NULL"))
    
    submission_number = Column(Integer, default=1)
    content = Column(Text)
    attachments = Column(JSON)  # Array of file URLs
    submitted_at = Column(DateTime)
    status = Column(SQLEnum(SubmissionStatus), nullable=False, default=SubmissionStatus.NOT_SUBMITTED)
    is_late = Column(Boolean, default=False)
    score = Column(Float)
    feedback = Column(Text)
    graded_by_id = Column(Integer, ForeignKey("public.users.id"))
    graded_at = Column(DateTime)
    plagiarism_score = Column(Float)
    remarks = Column(Text)

    # Relationships
    section_assignment = relationship("SectionAssignment", back_populates="submissions")
    student = relationship("StudentProfile")
    group = relationship("AssignmentGroup")
    graded_by = relationship("User")
    rubric_scores = relationship("RubricScore", back_populates="submission", cascade="all, delete-orphan")

class AssignmentGroup(BaseModel):
    __tablename__ = "assignment_groups"
    __table_args__ = {'schema': 'academic'}

    section_assignment_id = Column(Integer, ForeignKey("academic.section_assignments.id", ondelete="CASCADE"), nullable=False)
    leader_id = Column(Integer, ForeignKey("public.student_profiles.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    description = Column(Text)
    formed_at = Column(DateTime, nullable=False)

    # Relationships
    section_assignment = relationship("SectionAssignment")
    leader = relationship("StudentProfile", foreign_keys=[leader_id])
    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    submissions = relationship("AssignmentSubmission", back_populates="group")

class GroupMember(BaseModel):
    __tablename__ = "group_members"
    __table_args__ = (
        UniqueConstraint('group_id', 'student_id', name='uq_group_member'),
        {'schema': 'academic'}
    )

    group_id = Column(Integer, ForeignKey("academic.assignment_groups.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("public.student_profiles.id", ondelete="CASCADE"), nullable=False)
    
    role = Column(String)
    joined_at = Column(DateTime, nullable=False)
    contribution_score = Column(Float)  # Peer assessment score
    remarks = Column(Text)

    # Relationships
    group = relationship("AssignmentGroup", back_populates="members")
    student = relationship("StudentProfile")

class RubricScore(BaseModel):
    __tablename__ = "rubric_scores"
    __table_args__ = (
        UniqueConstraint(
            'submission_id', 'rubric_id',
            name='uq_rubric_score'
        ),
        {'schema': 'academic'}
    )

    submission_id = Column(Integer, ForeignKey("academic.assignment_submissions.id", ondelete="CASCADE"), nullable=False)
    rubric_id = Column(Integer, ForeignKey("academic.assignment_rubrics.id", ondelete="CASCADE"), nullable=False)
    
    score = Column(Float, nullable=False)
    comments = Column(Text)

    # Relationships
    submission = relationship("AssignmentSubmission", back_populates="rubric_scores")
    rubric = relationship("AssignmentRubric")