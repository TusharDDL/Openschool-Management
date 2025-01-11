from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException, status
import uuid

from app.models.fee import (
    FeeStructure, Discount, Payment, FeeType, PaymentStatus, FeeItem,
    StudentDiscount
)
from app.models.user import User
from app.schemas.fee import (
    FeeStructureCreate,
    FeeStructureUpdate,
    FeeDiscountCreate,
    FeeTransactionCreate,
    FeeReport
)

def create_fee_structure(
    db: Session,
    fee_data: FeeStructureCreate
) -> FeeStructure:
    fee_structure = FeeStructure(**fee_data.model_dump())
    db.add(fee_structure)
    db.commit()
    db.refresh(fee_structure)
    return fee_structure

def get_fee_structure(
    db: Session,
    fee_structure_id: int
) -> FeeStructure:
    fee_structure = db.query(FeeStructure).filter(
        FeeStructure.id == fee_structure_id
    ).first()
    if not fee_structure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee structure not found"
        )
    return fee_structure

def get_fee_structures(
    db: Session,
    school_id: int,
    class_id: Optional[int] = None,
    section_id: Optional[int] = None,
    fee_type: Optional[FeeType] = None
) -> List[FeeStructure]:
    query = db.query(FeeStructure).filter(FeeStructure.school_id == school_id)
    
    if class_id:
        query = query.filter(FeeStructure.class_id == class_id)
    if section_id:
        query = query.filter(FeeStructure.section_id == section_id)
    if fee_type:
        query = query.filter(FeeStructure.fee_type == fee_type)
    
    return query.all()

def update_fee_structure(
    db: Session,
    fee_structure_id: int,
    fee_data: FeeStructureUpdate
) -> FeeStructure:
    fee_structure = get_fee_structure(db, fee_structure_id)
    
    for field, value in fee_data.model_dump(exclude_unset=True).items():
        setattr(fee_structure, field, value)
    
    db.commit()
    db.refresh(fee_structure)
    return fee_structure

def create_discount(
    db: Session,
    discount_data: FeeDiscountCreate,
    approved_by: int
) -> Discount:
    # Verify fee structure exists
    get_fee_structure(db, discount_data.fee_structure_id)
    
    discount = Discount(
        **discount_data.model_dump(),
        approved_by=approved_by,
        start_date=date.today()
    )
    
    db.add(discount)
    db.commit()
    db.refresh(discount)
    return discount

def create_payment(
    db: Session,
    payment_data: FeeTransactionCreate
) -> Payment:
    # Generate unique transaction ID
    transaction_id = str(uuid.uuid4())
    
    payment = Payment(
        **payment_data.model_dump(),
        transaction_id=transaction_id,
        payment_date=date.today(),
        payment_status=PaymentStatus.COMPLETED
    )
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def get_fee_report(
    db: Session,
    report_params: FeeReport,
    school_id: int
) -> List[Payment]:
    query = db.query(Payment).join(
        FeeItem
    ).join(
        FeeStructure
    ).filter(
        FeeStructure.school_id == school_id,
        Payment.payment_date.between(
            report_params.start_date,
            report_params.end_date
        )
    )
    
    if report_params.student_id:
        query = query.join(
            FeeItem
        ).filter(
            FeeItem.student_id == report_params.student_id
        )
    
    if report_params.class_id:
        query = query.filter(
            FeeStructure.class_id == report_params.class_id
        )
    
    if report_params.fee_type:
        query = query.filter(
            FeeStructure.fee_type == report_params.fee_type
        )
    
    return query.all()

def get_student_pending_fees(
    db: Session,
    student_id: int,
    school_id: int
) -> List[FeeItem]:
    # Get all fee items for the student
    fee_items = db.query(FeeItem).join(
        FeeStructure
    ).filter(
        FeeStructure.school_id == school_id,
        FeeItem.student_id == student_id,
        FeeItem.is_paid == False
    ).all()
    
    # Calculate remaining amount for each fee item
    pending_items = []
    for item in fee_items:
        total_paid = db.query(func.sum(Payment.amount)).filter(
            Payment.fee_item_id == item.id,
            Payment.payment_status == PaymentStatus.COMPLETED
        ).scalar() or 0
        
        total_discount = db.query(func.sum(StudentDiscount.discount.discount_value)).join(
            StudentDiscount.discount
        ).filter(
            StudentDiscount.student_id == student_id,
            StudentDiscount.is_active == True,
            StudentDiscount.start_date <= date.today(),
            or_(
                StudentDiscount.end_date == None,
                StudentDiscount.end_date >= date.today()
            )
        ).scalar() or 0
        
        if total_paid + total_discount < item.amount:
            pending_items.append(item)
    
    return pending_items