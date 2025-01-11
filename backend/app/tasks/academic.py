from typing import List, Dict, Any
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.academic.homework import Assignment, AssignmentSubmission
from app.models.academic.timetable import ClassSchedule
from app.models.student import StudentAttendance
from app.core.realtime import notifications

@celery_app.task
def process_assignment_submission(submission_id: int):
    """Process a new assignment submission (e.g., check for plagiarism)"""
    with SessionLocal() as db:
        submission = db.query(AssignmentSubmission).filter_by(id=submission_id).first()
        if not submission:
            return

        # TODO: Implement plagiarism check
        submission.plagiarism_score = 0.0
        db.commit()

        # Notify teacher
        notifications.send_personal_notification.delay(
            submission.section_assignment.assignment.teacher_id,
            {
                "type": "NEW_SUBMISSION",
                "assignment_id": submission.section_assignment.assignment_id,
                "student_id": submission.student_id
            }
        )

@celery_app.task
def send_assignment_reminders():
    """Send reminders for upcoming assignments"""
    with SessionLocal() as db:
        # Find assignments due in the next 24 hours
        upcoming = db.query(Assignment).filter(
            Assignment.due_date <= datetime.utcnow() + timedelta(days=1),
            Assignment.status == AssignmentStatus.PUBLISHED
        ).all()

        for assignment in upcoming:
            for section_assignment in assignment.section_assignments:
                if not section_assignment.is_published:
                    continue

                # Get students who haven't submitted
                submissions = {s.student_id: s for s in section_assignment.submissions}
                for student in section_assignment.section.students:
                    if student.id not in submissions:
                        notifications.send_personal_notification.delay(
                            student.user_id,
                            {
                                "type": "ASSIGNMENT_REMINDER",
                                "assignment_id": assignment.id,
                                "due_date": assignment.due_date.isoformat()
                            }
                        )

@celery_app.task
def sync_attendance(date: str = None):
    """Sync attendance records with timetable"""
    target_date = datetime.strptime(date, "%Y-%m-%d").date() if date else datetime.utcnow().date()
    weekday = target_date.strftime("%A").upper()

    with SessionLocal() as db:
        # Get all scheduled classes for the day
        schedules = db.query(ClassSchedule).filter_by(weekday=weekday).all()

        for schedule in schedules:
            # Check if attendance records exist
            existing = db.query(StudentAttendance).filter_by(
                section_id=schedule.section_id,
                date=target_date
            ).first()

            if not existing:
                # Create attendance records for all students
                for student in schedule.section.students:
                    attendance = StudentAttendance(
                        tenant_id=schedule.tenant_id,
                        student_id=student.id,
                        section_id=schedule.section_id,
                        subject_id=schedule.subject_id,
                        teacher_id=schedule.teacher_id,
                        date=target_date,
                        status="ABSENT",  # Default to absent
                        marked_by=schedule.teacher_id
                    )
                    db.add(attendance)

        db.commit()

@celery_app.task
def generate_timetable_conflicts_report(timetable_id: int):
    """Generate a report of conflicts in a timetable"""
    with SessionLocal() as db:
        conflicts = []
        schedules = db.query(ClassSchedule).filter_by(timetable_id=timetable_id).all()

        # Group schedules by day and period
        by_day_period = {}
        for schedule in schedules:
            key = (schedule.weekday, schedule.period_id)
            if key not in by_day_period:
                by_day_period[key] = []
            by_day_period[key].append(schedule)

        # Check for conflicts
        for (day, period), day_schedules in by_day_period.items():
            # Check teacher conflicts
            teachers = {}
            for schedule in day_schedules:
                if schedule.teacher_id in teachers:
                    conflicts.append({
                        "type": "TEACHER_CONFLICT",
                        "day": day,
                        "period": period,
                        "teacher_id": schedule.teacher_id,
                        "schedule1_id": teachers[schedule.teacher_id].id,
                        "schedule2_id": schedule.id
                    })
                teachers[schedule.teacher_id] = schedule

            # Check section conflicts
            sections = {}
            for schedule in day_schedules:
                if schedule.section_id in sections:
                    conflicts.append({
                        "type": "SECTION_CONFLICT",
                        "day": day,
                        "period": period,
                        "section_id": schedule.section_id,
                        "schedule1_id": sections[schedule.section_id].id,
                        "schedule2_id": schedule.id
                    })
                sections[schedule.section_id] = schedule

        return conflicts