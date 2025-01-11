from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, JSON, DateTime, UniqueConstraint, Float, Date
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class EmploymentType(str, Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    TEMPORARY = "TEMPORARY"
    INTERN = "INTERN"
    CONSULTANT = "CONSULTANT"

class EmploymentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PROBATION = "PROBATION"
    NOTICE_PERIOD = "NOTICE_PERIOD"
    TERMINATED = "TERMINATED"
    RESIGNED = "RESIGNED"
    RETIRED = "RETIRED"
    ON_LEAVE = "ON_LEAVE"
    SUSPENDED = "SUSPENDED"

class LeaveType(str, Enum):
    CASUAL = "CASUAL"
    SICK = "SICK"
    ANNUAL = "ANNUAL"
    MATERNITY = "MATERNITY"
    PATERNITY = "PATERNITY"
    STUDY = "STUDY"
    UNPAID = "UNPAID"
    COMPENSATORY = "COMPENSATORY"
    OTHER = "OTHER"

class LeaveStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    WITHDRAWN = "WITHDRAWN"

class StaffProfile(BaseModel):
    __tablename__ = "staff_profiles"
    __table_args__ = {'schema': 'staff'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    department_id = Column(Integer, ForeignKey("staff.departments.id", ondelete="SET NULL"))
    reporting_to_id = Column(Integer, ForeignKey("public.users.id", ondelete="SET NULL"))
    
    employee_id = Column(String, nullable=False)
    employment_type = Column(SQLEnum(EmploymentType), nullable=False)
    employment_status = Column(SQLEnum(EmploymentStatus), nullable=False)
    designation = Column(String, nullable=False)
    join_date = Column(Date, nullable=False)
    probation_end_date = Column(Date)
    confirmation_date = Column(Date)
    termination_date = Column(Date)
    notice_period_days = Column(Integer)
    work_location = Column(String)
    work_hours = Column(JSON)  # Working hours configuration
    skills = Column(JSON)  # List of skills and proficiency
    qualifications = Column(JSON)  # Academic and professional qualifications
    certifications = Column(JSON)  # Professional certifications
    emergency_contacts = Column(JSON)
    bank_details = Column(JSON)
    documents = Column(JSON)  # Employee documents
    metadata = Column(JSON)  # Additional configurable fields

    # Relationships
    tenant = relationship("Tenant")
    user = relationship("User", foreign_keys=[user_id])
    department = relationship("Department", back_populates="staff")
    reporting_to = relationship("User", foreign_keys=[reporting_to_id])
    leaves = relationship("Leave", back_populates="staff")
    attendance = relationship("StaffAttendance", back_populates="staff")
    performance_reviews = relationship("PerformanceReview", back_populates="staff")

class Department(BaseModel):
    __tablename__ = "departments"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'code', name='uq_department_code'),
        {'schema': 'staff'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    school_id = Column(Integer, ForeignKey("public.schools.id", ondelete="CASCADE"), nullable=False)
    head_id = Column(Integer, ForeignKey("public.users.id", ondelete="SET NULL"))
    parent_id = Column(Integer, ForeignKey("staff.departments.id", ondelete="SET NULL"))
    
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    description = Column(Text)
    is_academic = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    school = relationship("School")
    head = relationship("User")
    parent = relationship("Department", remote_side=[id])
    staff = relationship("StaffProfile", back_populates="department")

class Leave(BaseModel):
    __tablename__ = "leaves"
    __table_args__ = {'schema': 'staff'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.staff_profiles.id", ondelete="CASCADE"), nullable=False)
    approved_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="SET NULL"))
    
    leave_type = Column(SQLEnum(LeaveType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    half_day = Column(Boolean, default=False)
    reason = Column(Text, nullable=False)
    status = Column(SQLEnum(LeaveStatus), nullable=False, default=LeaveStatus.PENDING)
    attachments = Column(JSON)  # Supporting documents
    approval_notes = Column(Text)
    cancellation_reason = Column(Text)
    is_paid = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    staff = relationship("StaffProfile", back_populates="leaves")
    approved_by = relationship("User")

class LeaveBalance(BaseModel):
    __tablename__ = "leave_balances"
    __table_args__ = (
        UniqueConstraint('staff_id', 'leave_type', 'year', name='uq_leave_balance'),
        {'schema': 'staff'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.staff_profiles.id", ondelete="CASCADE"), nullable=False)
    
    leave_type = Column(SQLEnum(LeaveType), nullable=False)
    year = Column(Integer, nullable=False)
    total_days = Column(Float, nullable=False)
    used_days = Column(Float, default=0)
    pending_days = Column(Float, default=0)  # Days in pending leave requests
    carried_forward = Column(Float, default=0)
    expires_on = Column(Date)  # For carried forward leaves

    # Relationships
    tenant = relationship("Tenant")
    staff = relationship("StaffProfile")

class StaffAttendance(BaseModel):
    __tablename__ = "staff_attendance"
    __table_args__ = (
        UniqueConstraint('staff_id', 'date', name='uq_staff_attendance'),
        {'schema': 'staff'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.staff_profiles.id", ondelete="CASCADE"), nullable=False)
    
    date = Column(Date, nullable=False)
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    status = Column(String, nullable=False)  # Present, Absent, Half Day, On Leave
    work_hours = Column(Float)
    overtime_hours = Column(Float, default=0)
    late_minutes = Column(Integer, default=0)
    early_leaving_minutes = Column(Integer, default=0)
    ip_address = Column(String)
    location = Column(String)
    device_info = Column(JSON)
    remarks = Column(Text)

    # Relationships
    tenant = relationship("Tenant")
    staff = relationship("StaffProfile", back_populates="attendance")

class PerformanceReview(BaseModel):
    __tablename__ = "performance_reviews"
    __table_args__ = {'schema': 'staff'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.staff_profiles.id", ondelete="CASCADE"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    review_period_start = Column(Date, nullable=False)
    review_period_end = Column(Date, nullable=False)
    review_type = Column(String, nullable=False)  # Annual, Probation, Quarterly
    review_date = Column(Date, nullable=False)
    overall_rating = Column(Float)
    strengths = Column(Text)
    areas_for_improvement = Column(Text)
    goals = Column(JSON)
    achievements = Column(JSON)
    training_needs = Column(Text)
    reviewer_comments = Column(Text)
    staff_comments = Column(Text)
    next_review_date = Column(Date)
    status = Column(String, nullable=False)  # Draft, In Review, Completed
    attachments = Column(JSON)

    # Relationships
    tenant = relationship("Tenant")
    staff = relationship("StaffProfile", back_populates="performance_reviews")
    reviewer = relationship("User")
    ratings = relationship("PerformanceRating", back_populates="review", cascade="all, delete-orphan")

class PerformanceRating(BaseModel):
    __tablename__ = "performance_ratings"
    __table_args__ = (
        UniqueConstraint('review_id', 'category', name='uq_performance_rating'),
        {'schema': 'staff'}
    )

    review_id = Column(Integer, ForeignKey("staff.performance_reviews.id", ondelete="CASCADE"), nullable=False)
    
    category = Column(String, nullable=False)  # e.g., Communication, Leadership, etc.
    rating = Column(Float, nullable=False)
    weight = Column(Float, default=1.0)
    comments = Column(Text)

    # Relationships
    review = relationship("PerformanceReview", back_populates="ratings")