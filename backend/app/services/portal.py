from typing import List, Optional
from datetime import datetime, date, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.attendance import AttendanceRecord, AttendanceStatus
from app.models.assignment import Assignment, AssignmentSubmission, SubmissionStatus
from app.models.fee import FeeTransaction, PaymentStatus
from app.models.academic import Result, Assessment
from app.schemas.dashboard import (
    StudentDashboard,
    AttendanceSummary,
    AssignmentSummary,
    FeeSummary,
    AcademicSummary,
    StudentAssignments,
    ResultDetail
)

def get_attendance_summary(db: Session, student_id: int, days: int = 30) -> AttendanceSummary:
    start_date = date.today() - timedelta(days=days)
    
    # Get attendance records
    records = db.query(AttendanceRecord).join(
        AttendanceRecord.session
    ).filter(
        AttendanceRecord.student_id == student_id,
        AttendanceRecord.session.date >= start_date
    ).all()
    
    total_days = len(records)
    present_days = sum(1 for r in records if r.status == AttendanceStatus.PRESENT)
    absent_days = sum(1 for r in records if r.status == AttendanceStatus.ABSENT)
    late_days = sum(1 for r in records if r.status == AttendanceStatus.LATE)
    
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
    recent_attendance = [r.status for r in records[-5:]] if records else []
    
    return AttendanceSummary(
        total_days=total_days,
        present_days=present_days,
        absent_days=absent_days,
        late_days=late_days,
        attendance_percentage=attendance_percentage,
        recent_attendance=recent_attendance
    )

def get_assignment_summary(db: Session, student_id: int) -> AssignmentSummary:
    # Get all assignments for student's class
    assignments = db.query(Assignment).join(
        AssignmentSubmission,
        isouter=True
    ).filter(
        Assignment.class_id == db.query(User).filter(
            User.id == student_id
        ).first().class_id
    ).all()
    
    total = len(assignments)
    completed = sum(1 for a in assignments if any(
        s.student_id == student_id and s.status in [SubmissionStatus.SUBMITTED, SubmissionStatus.GRADED]
        for s in a.submissions
    ))
    pending = sum(1 for a in assignments if not any(
        s.student_id == student_id
        for s in a.submissions
    ))
    overdue = sum(1 for a in assignments if (
        not any(s.student_id == student_id for s in a.submissions) and
        a.due_date < datetime.utcnow() and
        not a.allow_late_submission
    ))
    
    recent = [
        {
            "id": a.id,
            "title": a.title,
            "due_date": a.due_date,
            "status": next(
                (s.status for s in a.submissions if s.student_id == student_id),
                SubmissionStatus.PENDING
            )
        }
        for a in sorted(assignments, key=lambda x: x.due_date, reverse=True)[:5]
    ]
    
    return AssignmentSummary(
        total_assignments=total,
        completed_assignments=completed,
        pending_assignments=pending,
        overdue_assignments=overdue,
        recent_assignments=recent
    )

def get_fee_summary(db: Session, student_id: int) -> FeeSummary:
    # Get all fee transactions
    transactions = db.query(FeeTransaction).join(
        FeeTransaction.fee_structure
    ).filter(
        FeeTransaction.student_id == student_id
    ).all()
    
    total_fees = sum(t.fee_structure.amount for t in transactions)
    paid_amount = sum(t.amount_paid for t in transactions if t.status == PaymentStatus.PAID)
    pending_amount = total_fees - paid_amount
    
    # Get overdue amounts
    overdue_amount = sum(
        t.fee_structure.amount - sum(
            pt.amount_paid for pt in t.fee_structure.fee_transactions
            if pt.student_id == student_id and pt.status == PaymentStatus.PAID
        )
        for t in transactions
        if t.fee_structure.due_date < date.today()
    )
    
    # Find next due date
    next_due = min(
        (t.fee_structure.due_date for t in transactions
         if t.fee_structure.due_date > date.today()),
        default=None
    )
    
    return FeeSummary(
        total_fees=total_fees,
        paid_amount=paid_amount,
        pending_amount=pending_amount,
        overdue_amount=overdue_amount,
        next_due_date=next_due,
        payment_status=PaymentStatus.PAID if pending_amount == 0 else PaymentStatus.PENDING
    )

def get_academic_summary(db: Session, student_id: int) -> AcademicSummary:
    # Get all results
    results = db.query(Result).join(
        Assessment
    ).filter(
        Result.student_id == student_id
    ).all()
    
    # Calculate current average
    total_percentage = 0
    total_assessments = 0
    subject_scores = {}
    
    for result in results:
        percentage = (result.marks_obtained / result.assessment.total_marks) * 100
        subject_id = result.assessment.subject_id
        
        if subject_id not in subject_scores:
            subject_scores[subject_id] = []
        subject_scores[subject_id].append(percentage)
        
        total_percentage += percentage
        total_assessments += 1
    
    current_average = total_percentage / total_assessments if total_assessments > 0 else 0
    
    # Calculate subject averages
    subject_averages = {
        subject_id: sum(scores) / len(scores)
        for subject_id, scores in subject_scores.items()
    }
    
    # Get subject names
    subjects = db.query(Subject).filter(
        Subject.id.in_(subject_scores.keys())
    ).all()
    subject_names = {s.id: s.name for s in subjects}
    
    # Identify subjects at risk (below 60%) and top subjects
    subjects_at_risk = [
        subject_names[sid]
        for sid, avg in subject_averages.items()
        if avg < 60
    ]
    
    top_subjects = [
        subject_names[sid]
        for sid, avg in sorted(
            subject_averages.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
    ]
    
    # Get recent assessments
    recent_assessments = [
        {
            "subject": result.assessment.subject.name,
            "title": result.assessment.name,
            "marks": result.marks_obtained,
            "total": result.assessment.total_marks,
            "date": result.created_at
        }
        for result in sorted(results, key=lambda x: x.created_at, reverse=True)[:5]
    ]
    
    return AcademicSummary(
        current_average=current_average,
        subjects_at_risk=subjects_at_risk,
        top_subjects=top_subjects,
        recent_assessments=recent_assessments
    )

def get_student_dashboard(db: Session, student_id: int) -> StudentDashboard:
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return StudentDashboard(
        student_id=student.id,
        name=student.username,
        class_name=student.class_.name,
        section_name=student.section.name if student.section else None,
        attendance=get_attendance_summary(db, student_id),
        assignments=get_assignment_summary(db, student_id),
        fees=get_fee_summary(db, student_id),
        academics=get_academic_summary(db, student_id)
    )

def get_student_assignments(db: Session, student_id: int) -> StudentAssignments:
    submissions = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.student_id == student_id
    ).all()
    
    # Get all assignments for student's class
    class_id = db.query(User).filter(User.id == student_id).first().class_id
    assignments = db.query(Assignment).filter(
        Assignment.class_id == class_id
    ).all()
    
    # Create lookup for submissions
    submission_lookup = {
        s.assignment_id: s for s in submissions
    }
    
    pending = []
    submitted = []
    graded = []
    
    for assignment in assignments:
        submission = submission_lookup.get(assignment.id)
        
        detail = AssignmentDetail(
            id=assignment.id,
            title=assignment.title,
            subject=assignment.subject.name,
            due_date=assignment.due_date,
            status=submission.status if submission else SubmissionStatus.PENDING,
            score=submission.score if submission else None,
            max_score=assignment.max_score,
            file_url=submission.file_url if submission else None,
            feedback=submission.feedback if submission else None
        )
        
        if not submission:
            pending.append(detail)
        elif submission.status == SubmissionStatus.GRADED:
            graded.append(detail)
        else:
            submitted.append(detail)
    
    return StudentAssignments(
        pending=pending,
        submitted=submitted,
        graded=graded
    )

def submit_assignment(
    db: Session,
    student_id: int,
    assignment_id: int,
    file_url: str,
    comments: Optional[str] = None
) -> AssignmentSubmission:
    # Verify assignment exists and is open
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    if assignment.status == AssignmentStatus.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment is closed"
        )
    
    # Check if past due date
    is_late = datetime.utcnow() > assignment.due_date
    if is_late and not assignment.allow_late_submission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Late submissions are not allowed"
        )
    
    # Create or update submission
    submission = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.assignment_id == assignment_id,
        AssignmentSubmission.student_id == student_id
    ).first()
    
    if submission:
        submission.file_url = file_url
        submission.comments = comments
        submission.submission_date = datetime.utcnow()
        submission.status = SubmissionStatus.LATE if is_late else SubmissionStatus.SUBMITTED
    else:
        submission = AssignmentSubmission(
            assignment_id=assignment_id,
            student_id=student_id,
            file_url=file_url,
            comments=comments,
            status=SubmissionStatus.LATE if is_late else SubmissionStatus.SUBMITTED
        )
        db.add(submission)
    
    db.commit()
    db.refresh(submission)
    return submission