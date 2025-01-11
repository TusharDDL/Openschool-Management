from enum import Enum
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"

class StudentProfile(BaseModel):
    __tablename__ = "student_profiles"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    admission_number = Column(String, unique=True, index=True)
    admission_date = Column(Date, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(SQLEnum(Gender), nullable=False)
    blood_group = Column(SQLEnum(BloodGroup))
    address = Column(String, nullable=False)
    phone = Column(String)
    emergency_contact = Column(String, nullable=False)
    medical_conditions = Column(String)
    previous_school = Column(String)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant", back_populates="students")
    user = relationship("User", back_populates="student_profile")
    guardians = relationship("Guardian", back_populates="student")
    documents = relationship("StudentDocument", back_populates="student")
    notes = relationship("StudentNote", back_populates="student")

class Guardian(BaseModel):
    __tablename__ = "guardians"

    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    relation_type = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    occupation = Column(String)
    phone = Column(String, nullable=False)
    email = Column(String)
    address = Column(String)
    is_emergency_contact = Column(Boolean, default=False)
    is_authorized_pickup = Column(Boolean, default=False)

    # Relationships
    student = relationship("StudentProfile", back_populates="guardians")
    user = relationship("User", back_populates="guardian_profile")

class StudentDocument(BaseModel):
    __tablename__ = "student_documents"

    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    verified_by = Column(Integer, ForeignKey("users.id"))
    
    document_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    document_url = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    verification_date = Column(Date)

    # Relationships
    student = relationship("StudentProfile", back_populates="documents")
    uploader = relationship("User", foreign_keys=[uploaded_by])
    verifier = relationship("User", foreign_keys=[verified_by])

class StudentNote(BaseModel):
    __tablename__ = "student_notes"

    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    note_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_confidential = Column(Boolean, default=False)

    # Relationships
    student = relationship("StudentProfile", back_populates="notes")
    author = relationship("User", back_populates="student_notes")

class StudentAttendance(BaseModel):
    __tablename__ = "student_attendance"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)  # present, absent, late, excused
    remarks = Column(String)
    marked_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    tenant = relationship("Tenant")
    student = relationship("StudentProfile")
    marker = relationship("User", foreign_keys=[marked_by])