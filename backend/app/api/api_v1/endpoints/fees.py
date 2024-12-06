from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import io
import pandas as pd

from app.api.deps import get_db
from app.core.security import require_school_admin, get_current_user
from app.models.user import User
from app.models.fee import FeeType, PaymentInterval
from app.schemas.fee import (
    FeeStructureCreate,
    FeeStructureUpdate,
    FeeStructureInDB,
    FeeDiscountCreate,
    FeeDiscountInDB,
    FeeTransactionCreate,
    FeeTransactionInDB,
    FeeReport
)
from app.services import fee as fee_service

router = APIRouter()

@router.post("", response_model=FeeStructureInDB)
async def create_fee_structure(
    fee_data: FeeStructureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin)
) -> FeeStructureInDB:
    """
    Create a new fee structure (School Admin only)
    """
    if current_user.school_id != fee_data.school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create fee structure for different school"
        )
    return fee_service.create_fee_structure(db, fee_data)

@router.get("", response_model=List[FeeStructureInDB])
async def list_fee_structures(
    class_id: int | None = Query(None, description="Filter by class ID"),
    section_id: int | None = Query(None, description="Filter by section ID"),
    fee_type: FeeType | None = Query(None, description="Filter by fee type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[FeeStructureInDB]:
    """
    List fee structures with optional filters
    """
    return fee_service.get_fee_structures(
        db,
        school_id=current_user.school_id,
        class_id=class_id,
        section_id=section_id,
        fee_type=fee_type
    )

@router.post("/discounts", response_model=FeeDiscountInDB)
async def create_fee_discount(
    discount_data: FeeDiscountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin)
) -> FeeDiscountInDB:
    """
    Create a fee discount (School Admin only)
    """
    return fee_service.create_fee_discount(
        db,
        discount_data,
        approved_by=current_user.id
    )

@router.post("/pay", response_model=FeeTransactionInDB)
async def record_fee_payment(
    payment_data: FeeTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FeeTransactionInDB:
    """
    Record a fee payment
    """
    # Verify the fee structure belongs to user's school
    fee_structure = fee_service.get_fee_structure(db, payment_data.fee_structure_id)
    if fee_structure.school_id != current_user.school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot process payment for different school"
        )
    
    return fee_service.create_fee_transaction(db, payment_data)

@router.get("/student/{student_id}/pending")
async def get_student_pending_fees(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[FeeStructureInDB]:
    """
    Get pending fees for a student
    """
    return fee_service.get_student_pending_fees(
        db,
        student_id=student_id,
        school_id=current_user.school_id
    )

@router.post("/report")
async def generate_fee_report(
    report_params: FeeReport,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_school_admin)
) -> StreamingResponse:
    """
    Generate fee report in Excel format
    """
    transactions = fee_service.get_fee_report(
        db,
        report_params,
        school_id=current_user.school_id
    )
    
    # Convert to DataFrame
    df = pd.DataFrame([
        {
            "Transaction ID": t.transaction_id,
            "Student ID": t.student_id,
            "Amount": t.amount_paid,
            "Payment Date": t.payment_date,
            "Payment Method": t.payment_method,
            "Status": t.status,
            "Fee Type": t.fee_structure.fee_type,
            "Academic Year": t.fee_structure.academic_year
        }
        for t in transactions
    ])
    
    # Create Excel file
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=fee_report_{date.today()}.xlsx"
        }
    )