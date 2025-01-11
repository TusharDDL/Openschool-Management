from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Term(BaseModel):
    __tablename__ = "terms"
    __table_args__ = (
        {'schema': 'academic'},  # Using schema for better organization
        UniqueConstraint('academic_year_id', 'name', name='uq_term_name')
    )

    academic_year_id = Column(Integer, ForeignKey("academic.academic_years.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)  # e.g., "Term 1", "First Semester"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    description = Column(String)

    # Relationships
    academic_year = relationship("AcademicYear", back_populates="terms")
    exams = relationship("Exam", back_populates="term", cascade="all, delete-orphan")
    fee_schedules = relationship("FeeSchedule", back_populates="term")