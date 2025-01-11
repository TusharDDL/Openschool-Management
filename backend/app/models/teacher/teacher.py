from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, Date
from sqlalchemy.orm import relationship
from app.models.base import TenantModel

# Association table for teacher-subject relationship
teacher_subject = Table(
    'teacher_subject',
    TenantModel.metadata,
    Column('teacher_id', Integer, ForeignKey('teachers.id'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('subjects.id'), primary_key=True)
)

class Teacher(TenantModel):
    __tablename__ = "teachers"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    employee_id = Column(String)
    phone = Column(String)
    address = Column(String)
    qualification = Column(String)
    experience_years = Column(Integer)
    joining_date = Column(Date)
    is_active = Column(Boolean, default=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="teacher")
    school = relationship("School", back_populates="teachers")
    subjects = relationship(
        "Subject",
        secondary=teacher_subject,
        back_populates="teachers"
    )
    sections = relationship("TeacherSection", back_populates="teacher")
    timetable_entries = relationship("TimetableEntry", back_populates="teacher")
    assignments = relationship("Assignment", back_populates="teacher")

class TeacherSection(TenantModel):
    __tablename__ = "teacher_sections"

    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    is_class_teacher = Column(Boolean, default=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)

    # Relationships
    teacher = relationship("Teacher", back_populates="sections")
    section = relationship("Section", back_populates="teachers")
    subject = relationship("Subject", back_populates="teacher_sections")
    school = relationship("School", back_populates="teacher_sections")

class TeacherAttendance(TenantModel):
    __tablename__ = "teacher_attendance"

    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    date = Column(Date, nullable=False)
    is_present = Column(Boolean, default=True)
    remarks = Column(String)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)

    # Relationships
    teacher = relationship("Teacher", back_populates="attendance")
    school = relationship("School", back_populates="teacher_attendance")