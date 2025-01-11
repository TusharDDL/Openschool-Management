from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class AcademicYear(BaseModel):
    __tablename__ = "academic_years"
    __table_args__ = (
        {'schema': 'academic'}  # Using schema for better organization
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    is_current = Column(Boolean, default=False)
    description = Column(String)

    # Relationships
    tenant = relationship("Tenant", back_populates="academic_years")
    classes = relationship("Class", back_populates="academic_year", cascade="all, delete-orphan")
    terms = relationship("Term", back_populates="academic_year", cascade="all, delete-orphan")
    fee_structures = relationship("FeeStructure", back_populates="academic_year")

    # Unique constraint for name within a tenant
    __table_args__ = (
        {'schema': 'academic'},  # Using schema for better organization
        UniqueConstraint('tenant_id', 'name', name='uq_academic_year_name')
    )