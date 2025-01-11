from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Time, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import WeekDay

class Timetable(BaseModel):
    __tablename__ = "timetables"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    name = Column(String, nullable=False)
    effective_from = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant", back_populates="timetables")
    school = relationship("School", back_populates="timetables")
    academic_year = relationship("AcademicYear", back_populates="timetables")
    periods = relationship("TimetablePeriod", back_populates="timetable")

class TimetablePeriod(BaseModel):
    __tablename__ = "timetable_periods"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    timetable_id = Column(Integer, ForeignKey("timetables.id"), nullable=False)
    period_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    day = Column(SQLEnum(WeekDay), nullable=False)
    room = Column(String)

    # Relationships
    tenant = relationship("Tenant")
    timetable = relationship("Timetable", back_populates="periods")