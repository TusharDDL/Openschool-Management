from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import UserRole
from app.models.student import StudentProfile, Guardian, StudentNote, StudentAttendance
from app.models.academic_core import TeacherSection

class User(BaseModel):
    __tablename__ = "users"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # Store as string to avoid SQLite enum issues
    is_active = Column(Boolean, default=True, nullable=False)  # Changed to Boolean
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    created_tickets = relationship("SupportTicket", back_populates="created_by", foreign_keys="[SupportTicket.created_by_id]")
    ticket_comments = relationship("TicketComment", back_populates="user")
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    guardian_profile = relationship("Guardian", back_populates="user", uselist=False)
    student_notes = relationship("StudentNote", back_populates="author")
    teacher_sections = relationship("TeacherSection", back_populates="teacher")
    marked_attendance = relationship("StudentAttendance", back_populates="marker", foreign_keys="[StudentAttendance.marked_by]")