from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, DateTime, Table
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, Base

# Task dependencies association table
task_dependencies = Table(
    'task_dependencies',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('onboarding_tasks.id'), primary_key=True),
    Column('depends_on_id', Integer, ForeignKey('onboarding_tasks.id'), primary_key=True)
)

class OnboardingTaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"

class OnboardingTask(BaseModel):
    __tablename__ = "onboarding_tasks"

    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(OnboardingTaskStatus), nullable=False, default=OnboardingTaskStatus.PENDING)
    assigned_to_id = Column(Integer, ForeignKey("saas_admins.id"))
    due_date = Column(DateTime)
    completed_at = Column(DateTime)
    completion_notes = Column(Text)
    order = Column(Integer, nullable=False)  # For task sequence
    is_blocking = Column(Boolean, default=False)  # If this task blocks other tasks

    # Relationships
    school = relationship("School", backref="onboarding_tasks")
    assigned_to = relationship("SaaSAdmin", back_populates="assigned_tasks")
    # Task dependencies relationship
    dependencies = relationship(
        "OnboardingTask",
        secondary=task_dependencies,
        primaryjoin="OnboardingTask.id==task_dependencies.c.task_id",
        secondaryjoin="OnboardingTask.id==task_dependencies.c.depends_on_id",
        backref="dependent_tasks",
        lazy="joined"
    )