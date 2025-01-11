from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class FeeType(str, Enum):
    TUITION = "TUITION"
    ADMISSION = "ADMISSION"
    EXAM = "EXAM"
    TRANSPORT = "TRANSPORT"
    LIBRARY = "LIBRARY"
    LABORATORY = "LABORATORY"
    SPORTS = "SPORTS"
    UNIFORM = "UNIFORM"
    BOOKS = "BOOKS"
    OTHER = "OTHER"

class PaymentInterval(str, Enum):
    ANNUAL = "ANNUAL"
    SEMI_ANNUAL = "SEMI_ANNUAL"
    QUARTERLY = "QUARTERLY"
    MONTHLY = "MONTHLY"
    ONE_TIME = "ONE_TIME"

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"

class PaymentMethod(str, Enum):
    CASH = "CASH"
    BANK_TRANSFER = "BANK_TRANSFER"
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    UPI = "UPI"
    WALLET = "WALLET"
    OTHER = "OTHER"

class FeeStructure(BaseModel):
    __tablename__ = "fee_structures"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    
    name = Column(String, nullable=False)
    fee_type = Column(SQLEnum(FeeType), nullable=False)
    amount = Column(Float, nullable=False)
    payment_interval = Column(SQLEnum(PaymentInterval), nullable=False)
    description = Column(String)
    is_optional = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    school = relationship("School")
    academic_year = relationship("AcademicYear")
    fee_items = relationship("FeeItem", back_populates="fee_structure")

class FeeItem(BaseModel):
    __tablename__ = "fee_items"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    is_paid = Column(Boolean, default=False)
    payment_date = Column(Date)
    payment_reference = Column(String)
    remarks = Column(String)

    # Relationships
    tenant = relationship("Tenant")
    student = relationship("StudentProfile")
    fee_structure = relationship("FeeStructure", back_populates="fee_items")
    payments = relationship("Payment", back_populates="fee_item")

class Payment(BaseModel):
    __tablename__ = "payments"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    fee_item_id = Column(Integer, ForeignKey("fee_items.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    transaction_id = Column(String)
    payment_status = Column(SQLEnum(PaymentStatus), nullable=False)
    payment_proof_url = Column(String)
    remarks = Column(String)

    # Relationships
    tenant = relationship("Tenant")
    fee_item = relationship("FeeItem", back_populates="payments")

class Discount(BaseModel):
    __tablename__ = "discounts"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    
    name = Column(String, nullable=False)
    description = Column(String)
    discount_type = Column(String, nullable=False)  # PERCENTAGE, FIXED_AMOUNT
    discount_value = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    school = relationship("School")
    student_discounts = relationship("StudentDiscount", back_populates="discount")

class StudentDiscount(BaseModel):
    __tablename__ = "student_discounts"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    discount_id = Column(Integer, ForeignKey("discounts.id"), nullable=False)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    remarks = Column(String)

    # Relationships
    tenant = relationship("Tenant")
    student = relationship("StudentProfile")
    discount = relationship("Discount", back_populates="student_discounts")