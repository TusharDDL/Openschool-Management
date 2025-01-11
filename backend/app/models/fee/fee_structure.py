from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import date
from app.models.base import TenantModel
from app.models.enums import FeeType, FeeStatus

class FeeStructure(TenantModel):
    __tablename__ = "fee_structures"

    name = Column(String, nullable=False)
    description = Column(String)
    amount = Column(Float, nullable=False)
    type = Column(Enum(FeeType), nullable=False)
    due_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"))

    # Relationships
    school = relationship("School", back_populates="fee_structures")
    class_ = relationship("Class", back_populates="fee_structures")
    fee_payments = relationship("FeePayment", back_populates="fee_structure")

class FeePayment(TenantModel):
    __tablename__ = "fee_payments"

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False, default=date.today)
    payment_method = Column(String)
    transaction_id = Column(String)
    status = Column(Enum(FeeStatus), nullable=False, default=FeeStatus.PENDING)
    remarks = Column(String)

    # Relationships
    student = relationship("Student", back_populates="fee_payments")
    fee_structure = relationship("FeeStructure", back_populates="fee_payments")

class FeeDiscount(TenantModel):
    __tablename__ = "fee_discounts"

    name = Column(String, nullable=False)
    description = Column(String)
    percentage = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)

    # Relationships
    school = relationship("School", back_populates="fee_discounts")
    student_discounts = relationship("StudentFeeDiscount", back_populates="discount")