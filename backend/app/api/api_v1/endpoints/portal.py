from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.dashboard import (
    StudentDashboard,
    StudentAssignments,
    ResultDetail
)
from app.services import portal as portal_service
from app.services import academic as academic_service

router = APIRouter()

@router.get("/dashboard", response_model=StudentDashboard)
async def get_student_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> StudentDashboard:
    """
    Get student dashboard data
    """
    return portal_service.get_student_dashboard(db, current_user.id)

@router.get("/assignments", response_model=StudentAssignments)
async def get_student_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> StudentAssignments:
    """
    Get student assignments grouped by status
    """
    return portal_service.get_student_assignments(db, current_user.id)

@router.post("/assignments/{assignment_id}/submit")
async def submit_assignment(
    assignment_id: int,
    file: UploadFile = File(...),
    comments: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit an assignment
    """
    # Here you would typically:
    # 1. Upload the file to your storage service (S3, etc.)
    # 2. Get the file URL
    # For this example, we'll use a dummy URL
    file_url = f"https://storage.example.com/assignments/{assignment_id}/{file.filename}"
    
    return portal_service.submit_assignment(
        db,
        student_id=current_user.id,
        assignment_id=assignment_id,
        file_url=file_url,
        comments=comments
    )

@router.get("/results", response_model=List[ResultDetail])
async def get_student_results(
    class_id: int | None = None,
    subject_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[ResultDetail]:
    """
    Get student results with optional filters
    """
    results = academic_service.get_student_results(
        db,
        school_id=current_user.school_id,
        student_id=current_user.id,
        class_id=class_id,
        subject_id=subject_id
    )
    
    # Group results by subject
    subject_results = {}
    for result in results:
        subject_id = result.assessment.subject_id
        if subject_id not in subject_results:
            subject_results[subject_id] = []
        subject_results[subject_id].append(result)
    
    # Calculate detailed results for each subject
    detailed_results = []
    for subject_id, subject_results in subject_results.items():
        subject = subject_results[0].assessment.subject
        
        # Calculate total percentage
        total_percentage = academic_service.calculate_final_result(
            db,
            school_id=current_user.school_id,
            student_id=current_user.id,
            class_id=subject_results[0].assessment.class_id,
            subject_id=subject_id
        )
        
        # Get class average
        class_average = db.query(func.avg(Result.marks_obtained)).join(
            Assessment
        ).filter(
            Assessment.subject_id == subject_id,
            Assessment.class_id == subject_results[0].assessment.class_id
        ).scalar() or 0
        
        # Calculate rank
        rank = 1
        class_results = db.query(
            Result.student_id,
            func.avg(Result.marks_obtained / Assessment.total_marks * 100)
        ).join(Assessment).filter(
            Assessment.subject_id == subject_id,
            Assessment.class_id == subject_results[0].assessment.class_id
        ).group_by(Result.student_id).all()
        
        class_results.sort(key=lambda x: x[1], reverse=True)
        for i, (student_id, avg) in enumerate(class_results):
            if student_id == current_user.id:
                rank = i + 1
                break
        
        detailed_results.append(
            ResultDetail(
                subject=subject.name,
                assessments=[{
                    "name": r.assessment.name,
                    "type": r.assessment.type,
                    "marks_obtained": r.marks_obtained,
                    "total_marks": r.assessment.total_marks,
                    "percentage": (r.marks_obtained / r.assessment.total_marks) * 100,
                    "date": r.created_at
                } for r in subject_results],
                total_percentage=total_percentage,
                grade=subject_results[0].assessment.grading_system.get_grade(total_percentage),
                class_average=class_average,
                rank=rank
            )
        )
    
    return detailed_results