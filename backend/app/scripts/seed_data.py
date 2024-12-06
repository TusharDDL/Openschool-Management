import asyncio
from datetime import datetime, timedelta
import typer
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.core.auth import get_password_hash
from app.models.enums import UserRole
from app.models.user import User
from app.models.tenant import Tenant
from app.models.school import School
from app.models.academic import (
    GradingSystem,
    Assessment,
    Timetable,
    WeekDay,
    AssessmentType,
    GradeSystem
)
from app.models.fee import (
    FeeStructure,
    FeeType,
    PaymentInterval
)

settings = get_settings()

def create_test_data(db: Session):
    # Create tenant
    tenant = Tenant(name="Demo School District")
    db.add(tenant)
    db.flush()

    # Create school
    school = School(
        tenant_id=tenant.id,
        name="Demo High School",
        address="123 Education St",
        phone="555-0123"
    )
    db.add(school)
    db.flush()

    # Create super admin
    super_admin = User(
        tenant_id=tenant.id,
        username="superadmin",
        email="superadmin@demo.com",
        hashed_password=get_password_hash("superadmin123"),
        role=UserRole.SUPER_ADMIN,
        is_active=True
    )
    db.add(super_admin)

    # Create school admin
    school_admin = User(
        tenant_id=tenant.id,
        username="schooladmin",
        email="schooladmin@demo.com",
        hashed_password=get_password_hash("schooladmin123"),
        role=UserRole.SCHOOL_ADMIN,
        is_active=True
    )
    db.add(school_admin)

    # Create teacher
    teacher = User(
        tenant_id=tenant.id,
        username="teacher",
        email="teacher@demo.com",
        hashed_password=get_password_hash("teacher123"),
        role=UserRole.TEACHER,
        is_active=True
    )
    db.add(teacher)

    # Create student
    student = User(
        tenant_id=tenant.id,
        username="student",
        email="student@demo.com",
        hashed_password=get_password_hash("student123"),
        role=UserRole.STUDENT,
        is_active=True
    )
    db.add(student)

    # Create grading system
    grading_system = GradingSystem(
        school_id=school.id,
        name="Standard Grading",
        type=GradeSystem.PERCENTAGE,
        scale={
            "A": 90,
            "B": 80,
            "C": 70,
            "D": 60,
            "F": 0
        },
        passing_grade=60.0
    )
    db.add(grading_system)
    db.flush()

    # Create assessment
    assessment = Assessment(
        school_id=school.id,
        class_id=1,
        subject_id=1,
        teacher_id=teacher.id,
        grading_system_id=grading_system.id,
        name="Midterm Exam",
        type=AssessmentType.EXAM,
        total_marks=100,
        weightage=30,
        description="Covers chapters 1-5"
    )
    db.add(assessment)

    # Create timetable
    timetable = Timetable(
        school_id=school.id,
        class_id=1,
        subject_id=1,
        teacher_id=teacher.id,
        day=WeekDay.MONDAY,
        start_time=datetime.strptime("09:00", "%H:%M").time(),
        end_time=datetime.strptime("10:00", "%H:%M").time(),
        room="101"
    )
    db.add(timetable)

    # Create fee structure
    fee_structure = FeeStructure(
        school_id=school.id,
        name="Tuition Fee 2024",
        fee_type=FeeType.TUITION,
        amount=5000.00,
        interval=PaymentInterval.MONTHLY,
        class_id=1,
        academic_year="2024"
    )
    db.add(fee_structure)

    # Commit all changes
    db.commit()

def main():
    typer.echo("Creating test data...")
    db = SessionLocal()
    try:
        create_test_data(db)
        typer.echo("Test data created successfully!")
    except Exception as e:
        typer.echo(f"Error creating test data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    typer.run(main)