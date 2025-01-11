from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, JSON, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ReportType(str, Enum):
    ACADEMIC = "ACADEMIC"
    ATTENDANCE = "ATTENDANCE"
    FINANCIAL = "FINANCIAL"
    EXAM = "EXAM"
    TRANSPORT = "TRANSPORT"
    HOSTEL = "HOSTEL"
    LIBRARY = "LIBRARY"
    INVENTORY = "INVENTORY"
    CUSTOM = "CUSTOM"

class ReportFormat(str, Enum):
    PDF = "PDF"
    EXCEL = "EXCEL"
    CSV = "CSV"
    HTML = "HTML"

class ReportStatus(str, Enum):
    DRAFT = "DRAFT"
    SCHEDULED = "SCHEDULED"
    GENERATING = "GENERATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class ReportTemplate(BaseModel):
    __tablename__ = "report_templates"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'code', name='uq_report_template'),
        {'schema': 'reports'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    
    code = Column(String, nullable=False)  # Unique template identifier
    name = Column(String, nullable=False)
    description = Column(Text)
    report_type = Column(SQLEnum(ReportType), nullable=False)
    template_data = Column(JSON, nullable=False)  # Template definition
    parameters_schema = Column(JSON)  # JSON Schema for required parameters
    supported_formats = Column(String)  # JSON array of supported formats
    is_system = Column(Boolean, default=False)  # System templates can't be modified
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    reports = relationship("Report", back_populates="template")

class Report(BaseModel):
    __tablename__ = "reports"
    __table_args__ = {'schema': 'reports'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    template_id = Column(Integer, ForeignKey("reports.report_templates.id", ondelete="CASCADE"), nullable=False)
    created_by = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    description = Column(Text)
    parameters = Column(JSON)  # Actual parameters used
    status = Column(SQLEnum(ReportStatus), nullable=False, default=ReportStatus.DRAFT)
    scheduled_at = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String)  # Cron expression for recurring reports
    next_run = Column(DateTime)
    last_run = Column(DateTime)

    # Relationships
    tenant = relationship("Tenant")
    template = relationship("ReportTemplate", back_populates="reports")
    creator = relationship("User")
    outputs = relationship("ReportOutput", back_populates="report", cascade="all, delete-orphan")

class ReportOutput(BaseModel):
    __tablename__ = "report_outputs"
    __table_args__ = {'schema': 'reports'}

    report_id = Column(Integer, ForeignKey("reports.reports.id", ondelete="CASCADE"), nullable=False)
    
    format = Column(SQLEnum(ReportFormat), nullable=False)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer)
    file_url = Column(String, nullable=False)
    is_temporary = Column(Boolean, default=True)  # Temporary files are cleaned up periodically
    expiry_date = Column(DateTime)  # When to delete temporary files
    checksum = Column(String)  # For file integrity verification

    # Relationships
    report = relationship("Report", back_populates="outputs")

class ReportSchedule(BaseModel):
    __tablename__ = "report_schedules"
    __table_args__ = {'schema': 'reports'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    template_id = Column(Integer, ForeignKey("reports.report_templates.id", ondelete="CASCADE"), nullable=False)
    created_by = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    description = Column(Text)
    parameters = Column(JSON)
    schedule_type = Column(String, nullable=False)  # daily, weekly, monthly, custom
    schedule_config = Column(JSON, nullable=False)  # Schedule configuration
    formats = Column(String, nullable=False)  # JSON array of output formats
    recipients = Column(String)  # JSON array of email addresses
    is_active = Column(Boolean, default=True)
    last_run = Column(DateTime)
    next_run = Column(DateTime)

    # Relationships
    tenant = relationship("Tenant")
    template = relationship("ReportTemplate")
    creator = relationship("User")