from sqlalchemy.orm import configure_mappers
from app.models import (
    Base, BaseModel,
    User, Tenant, School,
    AcademicYear, Class, Section, Subject,
    StudentProfile, Guardian, StudentDocument, StudentNote, StudentAttendance,
    FeeStructure, FeeItem, Payment, Discount, StudentDiscount,
    SaaSAdmin, SupportTicket, TicketComment, OnboardingTask
)

def configure_models():
    """Configure all SQLAlchemy models"""
    configure_mappers()

    # Return all models for convenience
    return {
        'Base': Base,
        'BaseModel': BaseModel,
        'User': User,
        'Tenant': Tenant,
        'School': School,
        'AcademicYear': AcademicYear,
        'Class': Class,
        'Section': Section,
        'Subject': Subject,
        'StudentProfile': StudentProfile,
        'Guardian': Guardian,
        'StudentDocument': StudentDocument,
        'StudentNote': StudentNote,
        'StudentAttendance': StudentAttendance,
        'FeeStructure': FeeStructure,
        'FeeItem': FeeItem,
        'Payment': Payment,
        'Discount': Discount,
        'StudentDiscount': StudentDiscount,
        'SaaSAdmin': SaaSAdmin,
        'SupportTicket': SupportTicket,
        'TicketComment': TicketComment,
        'OnboardingTask': OnboardingTask
    }