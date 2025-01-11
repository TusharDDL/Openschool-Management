from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, JSON, DateTime, UniqueConstraint, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ResourceType(str, Enum):
    ROOM = "ROOM"  # Classrooms, labs, halls
    EQUIPMENT = "EQUIPMENT"  # Projectors, laptops, etc.
    VEHICLE = "VEHICLE"  # School buses, vans
    SPORTS = "SPORTS"  # Sports equipment
    LIBRARY = "LIBRARY"  # Library resources
    LAB = "LAB"  # Laboratory equipment
    OTHER = "OTHER"

class ResourceStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    IN_USE = "IN_USE"
    MAINTENANCE = "MAINTENANCE"
    RESERVED = "RESERVED"
    OUT_OF_ORDER = "OUT_OF_ORDER"
    RETIRED = "RETIRED"

class BookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CHECKED_OUT = "CHECKED_OUT"
    RETURNED = "RETURNED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

class Resource(BaseModel):
    __tablename__ = "resources"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'code', name='uq_resource_code'),
        {'schema': 'resource'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    school_id = Column(Integer, ForeignKey("public.schools.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("resource.resource_categories.id", ondelete="SET NULL"))
    
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)  # Unique identifier/barcode
    description = Column(Text)
    resource_type = Column(SQLEnum(ResourceType), nullable=False)
    status = Column(SQLEnum(ResourceStatus), nullable=False, default=ResourceStatus.AVAILABLE)
    location = Column(String)
    capacity = Column(Integer)  # For rooms
    quantity = Column(Integer, default=1)  # For equipment
    available_quantity = Column(Integer)
    specifications = Column(JSON)  # Technical specifications
    rules = Column(Text)  # Usage rules
    requires_approval = Column(Boolean, default=False)
    approver_roles = Column(JSON)  # List of roles that can approve
    booking_lead_time = Column(Integer)  # Minimum hours before booking
    max_booking_duration = Column(Integer)  # Maximum hours per booking
    cost_per_hour = Column(Float)  # For paid resources
    maintenance_schedule = Column(JSON)  # Maintenance intervals
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    school = relationship("School")
    category = relationship("ResourceCategory", back_populates="resources")
    bookings = relationship("ResourceBooking", back_populates="resource")
    maintenance_logs = relationship("MaintenanceLog", back_populates="resource")
    allocations = relationship("ResourceAllocation", back_populates="resource")

class ResourceCategory(BaseModel):
    __tablename__ = "resource_categories"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'name', name='uq_category_name'),
        {'schema': 'resource'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("resource.resource_categories.id", ondelete="SET NULL"))
    
    name = Column(String, nullable=False)
    description = Column(Text)
    resource_type = Column(SQLEnum(ResourceType))
    attributes = Column(JSON)  # Custom attributes for resources
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    parent = relationship("ResourceCategory", remote_side=[id])
    resources = relationship("Resource", back_populates="category")

class ResourceBooking(BaseModel):
    __tablename__ = "resource_bookings"
    __table_args__ = {'schema': 'resource'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resource.resources.id", ondelete="CASCADE"), nullable=False)
    booked_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    approved_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="SET NULL"))
    event_id = Column(Integer, ForeignKey("calendar.events.id", ondelete="SET NULL"))
    
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    quantity = Column(Integer, default=1)
    purpose = Column(Text, nullable=False)
    status = Column(SQLEnum(BookingStatus), nullable=False, default=BookingStatus.PENDING)
    approval_notes = Column(Text)
    check_out_time = Column(DateTime)
    check_in_time = Column(DateTime)
    checked_out_by_id = Column(Integer, ForeignKey("public.users.id"))
    checked_in_by_id = Column(Integer, ForeignKey("public.users.id"))
    condition_at_checkout = Column(Text)
    condition_at_checkin = Column(Text)
    cost = Column(Float)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(JSON)
    metadata = Column(JSON)

    # Relationships
    tenant = relationship("Tenant")
    resource = relationship("Resource", back_populates="bookings")
    booked_by = relationship("User", foreign_keys=[booked_by_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])
    checked_out_by = relationship("User", foreign_keys=[checked_out_by_id])
    checked_in_by = relationship("User", foreign_keys=[checked_in_by_id])
    event = relationship("Event")

class MaintenanceLog(BaseModel):
    __tablename__ = "maintenance_logs"
    __table_args__ = {'schema': 'resource'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resource.resources.id", ondelete="CASCADE"), nullable=False)
    performed_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    maintenance_type = Column(String, nullable=False)  # Routine, Repair, Inspection
    description = Column(Text, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    cost = Column(Float)
    parts_replaced = Column(JSON)
    next_maintenance_due = Column(DateTime)
    status = Column(String, nullable=False)  # Completed, In Progress, Scheduled
    attachments = Column(JSON)  # File URLs
    notes = Column(Text)

    # Relationships
    tenant = relationship("Tenant")
    resource = relationship("Resource", back_populates="maintenance_logs")
    performed_by = relationship("User")

class ResourceAllocation(BaseModel):
    __tablename__ = "resource_allocations"
    __table_args__ = {'schema': 'resource'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resource.resources.id", ondelete="CASCADE"), nullable=False)
    allocated_to_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    allocated_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    quantity = Column(Integer, default=1)
    purpose = Column(Text)
    is_permanent = Column(Boolean, default=False)
    notes = Column(Text)

    # Relationships
    tenant = relationship("Tenant")
    resource = relationship("Resource", back_populates="allocations")
    allocated_to = relationship("User", foreign_keys=[allocated_to_id])
    allocated_by = relationship("User", foreign_keys=[allocated_by_id])