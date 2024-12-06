from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
import uuid

from app.models.fee import FeeStructure, FeeDiscount, FeeTransaction, FeeType, PaymentStatus
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

def create_fee_discount(
    db: Session,
    discount_data: FeeDiscountCreate,
    approved_by: int
) -> FeeDiscount:
    # Verify fee structure exists
    get_fee_structure(db, discount_data.fee_structure_id)
    
    discount = FeeDiscount(
        **discount_data.model_dump(),
        approved_by=approved_by,
        approved_at=date.today()
    )
    
    db.add(discount)
    db.commit()
    db.refresh(discount)
    return discount

def create_fee_transaction(
    db: Session,
    transaction_data: FeeTransactionCreate
) -> FeeTransaction:
    # Generate unique transaction ID
    transaction_id = str(uuid.uuid4())
    
    transaction = FeeTransaction(
        **transaction_data.model_dump(),
        transaction_id=transaction_id,
        payment_date=date.today(),
        status=PaymentStatus.PAID
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_fee_report(
    db: Session,
    report_params: FeeReport,
    school_id: int
) -> List[FeeTransaction]:
    query = db.query(FeeTransaction).join(
        FeeStructure
    ).filter(
        FeeStructure.school_id == school_id,
        FeeTransaction.payment_date.between(
            report_params.start_date,
            report_params.end_date
        )
    )
    
    if report_params.student_id:
        query = query.filter(
            FeeTransaction.student_id == report_params.student_id
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
) -> List[FeeStructure]:
    # Get all fee structures applicable to the student
    fee_structures = db.query(FeeStructure).filter(
        FeeStructure.school_id == school_id,
        or_(
            FeeStructure.class_id == None,
            FeeStructure.class_id == db.query(User).filter(
                User.id == student_id
            ).first().class_id
        )
    ).all()
    
    # Filter out fully paid fees
    pending_fees = []
    for fee in fee_structures:
        total_paid = db.query(func.sum(FeeTransaction.amount_paid)).filter(
            FeeTransaction.fee_structure_id == fee.id,
            FeeTransaction.student_id == student_id,
            FeeTransaction.status == PaymentStatus.PAID
        ).scalar() or 0
        
        total_discount = db.query(func.sum(FeeDiscount.amount)).filter(
            FeeDiscount.fee_structure_id == fee.id,
            FeeDiscount.student_id == student_id
        ).scalar() or 0
        
        if total_paid + total_discount < fee.amount:
            pending_fees.append(fee)
    
    return pending_fees