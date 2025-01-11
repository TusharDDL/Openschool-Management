from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Enum as SQLEnum, Text, UniqueConstraint, Time
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class HostelType(str, Enum):
    BOYS = "BOYS"
    GIRLS = "GIRLS"
    STAFF = "STAFF"
    GUEST = "GUEST"

class RoomType(str, Enum):
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    TRIPLE = "TRIPLE"
    QUAD = "QUAD"
    DORMITORY = "DORMITORY"

class RoomStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    RESERVED = "RESERVED"
    MAINTENANCE = "MAINTENANCE"
    INACTIVE = "INACTIVE"

class Hostel(BaseModel):
    __tablename__ = "hostels"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'name', name='uq_hostel_name'),
        {'schema': 'hostel'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    school_id = Column(Integer, ForeignKey("public.schools.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    hostel_type = Column(SQLEnum(HostelType), nullable=False)
    warden_id = Column(Integer, ForeignKey("public.users.id"))
    capacity = Column(Integer, nullable=False)
    address = Column(String)
    description = Column(Text)
    facilities = Column(String)  # JSON array of facilities
    rules = Column(Text)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    school = relationship("School")
    warden = relationship("User")
    blocks = relationship("HostelBlock", back_populates="hostel", cascade="all, delete-orphan")

class HostelBlock(BaseModel):
    __tablename__ = "hostel_blocks"
    __table_args__ = (
        UniqueConstraint('hostel_id', 'name', name='uq_block_name'),
        {'schema': 'hostel'}
    )

    hostel_id = Column(Integer, ForeignKey("hostel.hostels.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    floor_count = Column(Integer, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    # Relationships
    hostel = relationship("Hostel", back_populates="blocks")
    rooms = relationship("Room", back_populates="block", cascade="all, delete-orphan")

class Room(BaseModel):
    __tablename__ = "rooms"
    __table_args__ = (
        UniqueConstraint('block_id', 'room_number', name='uq_room_number'),
        {'schema': 'hostel'}
    )

    block_id = Column(Integer, ForeignKey("hostel.hostel_blocks.id", ondelete="CASCADE"), nullable=False)
    
    room_number = Column(String, nullable=False)
    floor = Column(Integer, nullable=False)
    room_type = Column(SQLEnum(RoomType), nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(SQLEnum(RoomStatus), nullable=False, default=RoomStatus.AVAILABLE)
    facilities = Column(String)  # JSON array of facilities
    monthly_rent = Column(Float)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    # Relationships
    block = relationship("HostelBlock", back_populates="rooms")
    beds = relationship("Bed", back_populates="room", cascade="all, delete-orphan")
    allocations = relationship("RoomAllocation", back_populates="room", cascade="all, delete-orphan")

class Bed(BaseModel):
    __tablename__ = "beds"
    __table_args__ = (
        UniqueConstraint('room_id', 'bed_number', name='uq_bed_number'),
        {'schema': 'hostel'}
    )

    room_id = Column(Integer, ForeignKey("hostel.rooms.id", ondelete="CASCADE"), nullable=False)
    
    bed_number = Column(String, nullable=False)
    status = Column(SQLEnum(RoomStatus), nullable=False, default=RoomStatus.AVAILABLE)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    # Relationships
    room = relationship("Room", back_populates="beds")
    allocations = relationship("BedAllocation", back_populates="bed", cascade="all, delete-orphan")

class RoomAllocation(BaseModel):
    __tablename__ = "room_allocations"
    __table_args__ = {'schema': 'hostel'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("hostel.rooms.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("public.student_profiles.id", ondelete="CASCADE"), nullable=False)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    monthly_rent = Column(Float, nullable=False)
    security_deposit = Column(Float)
    is_active = Column(Boolean, default=True)
    remarks = Column(Text)

    # Relationships
    tenant = relationship("Tenant")
    room = relationship("Room", back_populates="allocations")
    student = relationship("StudentProfile")

class BedAllocation(BaseModel):
    __tablename__ = "bed_allocations"
    __table_args__ = {'schema': 'hostel'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    bed_id = Column(Integer, ForeignKey("hostel.beds.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("public.student_profiles.id", ondelete="CASCADE"), nullable=False)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    remarks = Column(Text)

    # Relationships
    tenant = relationship("Tenant")
    bed = relationship("Bed", back_populates="allocations")
    student = relationship("StudentProfile")

class HostelFee(BaseModel):
    __tablename__ = "hostel_fees"
    __table_args__ = {'schema': 'hostel'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("public.student_profiles.id", ondelete="CASCADE"), nullable=False)
    room_allocation_id = Column(Integer, ForeignKey("hostel.room_allocations.id", ondelete="CASCADE"), nullable=False)
    
    month = Column(Date, nullable=False)  # First day of the month
    amount = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0)
    due_date = Column(Date, nullable=False)
    payment_date = Column(Date)
    payment_reference = Column(String)
    is_paid = Column(Boolean, default=False)
    late_fee = Column(Float, default=0)
    remarks = Column(Text)

    # Relationships
    tenant = relationship("Tenant")
    student = relationship("StudentProfile")
    room_allocation = relationship("RoomAllocation")