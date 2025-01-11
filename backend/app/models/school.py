from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.academic_core import AcademicYear, Class, Subject
from app.models.saas import SupportTicket, OnboardingTask

class School(BaseModel):
    __tablename__ = "schools"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="schools")
    academic_years = relationship("AcademicYear", back_populates="school")
    classes = relationship("Class", back_populates="school")
    subjects = relationship("Subject", back_populates="school")
