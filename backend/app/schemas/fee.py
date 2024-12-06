from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional, List
from app.models.fee import FeeType, PaymentInterval, PaymentStatus
from app.schemas.base import TimestampSchema

class FeeStructureBase(BaseModel):
    name: str
    fee_type: FeeType
    amount: float = Field(gt=0)
    interval: PaymentInterval
    academic_year: str
    class_id: Optional[int] = None
    section_id: Optional[int] = None

class FeeStructureCreate(FeeStructureBase):
    school_id: int

class FeeStructureUpdate(FeeStructureBase):
    pass

class FeeStructureInDB(FeeStructureBase, TimestampSchema):
    id: int
    school_id: int

class FeeDiscountBase(BaseModel):
    amount: float = Field(gt=0)
    reason: str
    student_id: int

class FeeDiscountCreate(FeeDiscountBase):
    fee_structure_id: int

class FeeDiscountInDB(FeeDiscountBase, TimestampSchema):
    id: int
    fee_structure_id: int
    approved_by: int
    approved_at: date

class FeeTransactionBase(BaseModel):
    amount_paid: float = Field(gt=0)
    payment_method: str
    remarks: Optional[str] = None

class FeeTransactionCreate(FeeTransactionBase):
    fee_structure_id: int
    student_id: int

class FeeTransactionUpdate(BaseModel):
    status: PaymentStatus

class FeeTransactionInDB(FeeTransactionBase, TimestampSchema):
    id: int
    fee_structure_id: int
    student_id: int
    transaction_id: str
    payment_date: date
    status: PaymentStatus

class FeeReport(BaseModel):
    start_date: date
    end_date: date
    student_id: Optional[int] = None
    class_id: Optional[int] = None
    fee_type: Optional[FeeType] = None

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v