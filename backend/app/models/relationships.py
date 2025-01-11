"""
This module sets up all relationships between models.
"""

from sqlalchemy.orm import configure_mappers, relationship
from app.models.base import Base
from app.models.user import User
from app.models.tenant import Tenant
from app.models.school import School
from app.models.academic_core import AcademicYear, Class, Section, Subject
from app.models.academic_timetable import Timetable, TimetablePeriod
from app.models.student import StudentProfile, Guardian, StudentDocument, StudentNote, StudentAttendance
from app.models.fee import FeeStructure, FeeItem, Payment, Discount, StudentDiscount
from app.models.saas import SaaSAdmin, SupportTicket, TicketComment, OnboardingTask

def setup_relationships():
    """Set up all relationships between models"""
    # School relationships
    School.support_tickets = relationship("SupportTicket", back_populates="school")
    School.onboarding_tasks = relationship("OnboardingTask", back_populates="school")
    School.timetables = relationship("Timetable", back_populates="school")

    # SupportTicket relationships
    SupportTicket.school = relationship("School", back_populates="support_tickets")

    # OnboardingTask relationships
    OnboardingTask.school = relationship("School", back_populates="onboarding_tasks")

    # Academic Year relationships
    AcademicYear.timetables = relationship("Timetable", back_populates="academic_year")

    # Tenant relationships
    Tenant.timetables = relationship("Timetable", back_populates="tenant")

    # Configure all mappers
    configure_mappers()