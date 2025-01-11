from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Enum as SQLEnum, Text, UniqueConstraint, Time
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class VehicleType(str, Enum):
    BUS = "BUS"
    VAN = "VAN"
    MINI_BUS = "MINI_BUS"
    OTHER = "OTHER"

class VehicleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    MAINTENANCE = "MAINTENANCE"
    REPAIR = "REPAIR"
    INACTIVE = "INACTIVE"
    RETIRED = "RETIRED"

class Vehicle(BaseModel):
    __tablename__ = "vehicles"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'registration_number', name='uq_vehicle_registration'),
        {'schema': 'transport'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    school_id = Column(Integer, ForeignKey("public.schools.id", ondelete="CASCADE"), nullable=False)
    
    registration_number = Column(String, nullable=False)
    vehicle_type = Column(SQLEnum(VehicleType), nullable=False)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    chassis_number = Column(String)
    engine_number = Column(String)
    seating_capacity = Column(Integer, nullable=False)
    fuel_type = Column(String)
    insurance_number = Column(String)
    insurance_expiry = Column(Date)
    fitness_expiry = Column(Date)
    permit_expiry = Column(Date)
    status = Column(SQLEnum(VehicleStatus), nullable=False, default=VehicleStatus.ACTIVE)
    gps_device_id = Column(String)
    description = Column(Text)

    # Relationships
    tenant = relationship("Tenant")
    school = relationship("School")
    routes = relationship("Route", back_populates="vehicle")
    maintenance_records = relationship("VehicleMaintenance", back_populates="vehicle", cascade="all, delete-orphan")

class Route(BaseModel):
    __tablename__ = "routes"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'route_number', name='uq_route_number'),
        {'schema': 'transport'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    school_id = Column(Integer, ForeignKey("public.schools.id", ondelete="CASCADE"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("transport.vehicles.id", ondelete="CASCADE"), nullable=False)
    
    route_number = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    start_location = Column(String, nullable=False)
    end_location = Column(String, nullable=False)
    distance = Column(Float)  # in kilometers
    estimated_time = Column(Integer)  # in minutes
    morning_start_time = Column(Time, nullable=False)
    afternoon_start_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    school = relationship("School")
    vehicle = relationship("Vehicle", back_populates="routes")
    stops = relationship("RouteStop", back_populates="route", cascade="all, delete-orphan")
    assignments = relationship("TransportAssignment", back_populates="route", cascade="all, delete-orphan")

class RouteStop(BaseModel):
    __tablename__ = "route_stops"
    __table_args__ = (
        UniqueConstraint('route_id', 'stop_number', name='uq_route_stop'),
        {'schema': 'transport'}
    )

    route_id = Column(Integer, ForeignKey("transport.routes.id", ondelete="CASCADE"), nullable=False)
    
    stop_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    morning_time = Column(Time, nullable=False)
    afternoon_time = Column(Time, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    # Relationships
    route = relationship("Route", back_populates="stops")

class TransportAssignment(BaseModel):
    __tablename__ = "transport_assignments"
    __table_args__ = (
        UniqueConstraint('route_id', 'student_id', name='uq_transport_assignment'),
        {'schema': 'transport'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    route_id = Column(Integer, ForeignKey("transport.routes.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("public.student_profiles.id", ondelete="CASCADE"), nullable=False)
    pickup_stop_id = Column(Integer, ForeignKey("transport.route_stops.id", ondelete="CASCADE"), nullable=False)
    dropoff_stop_id = Column(Integer, ForeignKey("transport.route_stops.id", ondelete="CASCADE"), nullable=False)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    morning_pickup = Column(Boolean, default=True)
    afternoon_dropoff = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    remarks = Column(Text)

    # Relationships
    tenant = relationship("Tenant")
    route = relationship("Route", back_populates="assignments")
    student = relationship("StudentProfile")
    pickup_stop = relationship("RouteStop", foreign_keys=[pickup_stop_id])
    dropoff_stop = relationship("RouteStop", foreign_keys=[dropoff_stop_id])

class VehicleMaintenance(BaseModel):
    __tablename__ = "vehicle_maintenance"
    __table_args__ = {'schema': 'transport'}

    vehicle_id = Column(Integer, ForeignKey("transport.vehicles.id", ondelete="CASCADE"), nullable=False)
    
    maintenance_type = Column(String, nullable=False)  # Service, Repair, etc.
    date = Column(Date, nullable=False)
    odometer_reading = Column(Integer)
    description = Column(Text, nullable=False)
    cost = Column(Float)
    performed_by = Column(String)
    next_due_date = Column(Date)
    next_due_reading = Column(Integer)
    attachments = Column(String)  # JSON array of file URLs
    remarks = Column(Text)

    # Relationships
    vehicle = relationship("Vehicle", back_populates="maintenance_records")