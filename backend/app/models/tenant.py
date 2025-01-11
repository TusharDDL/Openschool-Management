from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.academic_core import Subject, AcademicYear, Class, Section
from app.models.student import StudentProfile
from app.models.fee import FeeStructure, FeeItem, Payment, Discount, StudentDiscount

class Tenant(BaseModel):
    __tablename__ = "tenants"

    name = Column(String, nullable=False, index=True)
    subdomain = Column(String, nullable=False, unique=True)
    
    # Relationships
    schools = relationship("School", back_populates="tenant", cascade="all, delete-orphan")
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    subjects = relationship("Subject", back_populates="tenant", cascade="all, delete-orphan")
    academic_years = relationship("AcademicYear", back_populates="tenant", cascade="all, delete-orphan")
    classes = relationship("Class", back_populates="tenant", cascade="all, delete-orphan")
    sections = relationship("Section", back_populates="tenant", cascade="all, delete-orphan")
    students = relationship("StudentProfile", back_populates="tenant", cascade="all, delete-orphan")
    fee_structures = relationship("FeeStructure", back_populates="tenant", cascade="all, delete-orphan")
    fee_items = relationship("FeeItem", back_populates="tenant", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="tenant", cascade="all, delete-orphan")
    discounts = relationship("Discount", back_populates="tenant", cascade="all, delete-orphan")
    student_discounts = relationship("StudentDiscount", back_populates="tenant", cascade="all, delete-orphan")