from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import TenantModel

# Association table for parent-student relationship
parent_student = Table(
    'parent_student',
    TenantModel.metadata,
    Column('parent_id', Integer, ForeignKey('parents.id'), primary_key=True),
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True)
)

class Parent(TenantModel):
    __tablename__ = "parents"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    alternate_phone = Column(String)
    occupation = Column(String)
    address = Column(String)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="parent")
    school = relationship("School", back_populates="parents")
    students = relationship(
        "Student",
        secondary=parent_student,
        back_populates="parents"
    )
    communications = relationship("Communication", back_populates="parent")

class ParentCommunication(TenantModel):
    __tablename__ = "parent_communications"

    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)

    # Relationships
    parent = relationship("Parent", back_populates="communications")
    school = relationship("School", back_populates="parent_communications")