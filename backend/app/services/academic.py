from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.academic import (
    Timetable,
    GradingSystem,
    Assessment,
    Result,
    TeacherNote
)
from app.schemas.academic import (
    TimetableCreate,
    TimetableUpdate,
    GradingSystemCreate,
    AssessmentCreate,
    ResultCreate,
    TeacherNoteCreate
)

def create_timetable(db: Session, timetable_data: TimetableCreate) -> Timetable:
    # Check for time slot conflicts
    existing = db.query(Timetable).filter(
        and_(
            Timetable.school_id == timetable_data.school_id,
            Timetable.class_id == timetable_data.class_id,
            Timetable.section_id == timetable_data.section_id,
            Timetable.day == timetable_data.day,
            Timetable.is_active == True,
            ((Timetable.start_time <= timetable_data.start_time) & 
             (Timetable.end_time > timetable_data.start_time)) |
            ((Timetable.start_time < timetable_data.end_time) & 
             (Timetable.end_time >= timetable_data.end_time))
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Time slot conflict detected"
        )
    
    timetable = Timetable(**timetable_data.model_dump())
    db.add(timetable)
    db.commit()
    db.refresh(timetable)
    return timetable

def get_timetable(
    db: Session,
    school_id: int,
    class_id: Optional[int] = None,
    section_id: Optional[int] = None,
    teacher_id: Optional[int] = None
) -> List[Timetable]:
    query = db.query(Timetable).filter(
        Timetable.school_id == school_id,
        Timetable.is_active == True
    )
    
    if class_id:
        query = query.filter(Timetable.class_id == class_id)
    if section_id:
        query = query.filter(Timetable.section_id == section_id)
    if teacher_id:
        query = query.filter(Timetable.teacher_id == teacher_id)
    
    return query.all()

def create_grading_system(
    db: Session,
    grading_data: GradingSystemCreate
) -> GradingSystem:
    grading_system = GradingSystem(**grading_data.model_dump())
    db.add(grading_system)
    db.commit()
    db.refresh(grading_system)
    return grading_system

def create_assessment(
    db: Session,
    assessment_data: AssessmentCreate
) -> Assessment:
    # Validate grading system exists and belongs to school
    grading_system = db.query(GradingSystem).filter(
        GradingSystem.id == assessment_data.grading_system_id,
        GradingSystem.school_id == assessment_data.school_id
    ).first()
    
    if not grading_system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grading system not found"
        )
    
    assessment = Assessment(**assessment_data.model_dump())
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment

def create_result(db: Session, result_data: ResultCreate) -> Result:
    # Validate assessment exists
    assessment = db.query(Assessment).filter(
        Assessment.id == result_data.assessment_id
    ).first()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Validate marks are within total marks
    if result_data.marks_obtained > assessment.total_marks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Marks obtained cannot exceed total marks"
        )
    
    result = Result(**result_data.model_dump())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

def get_student_results(
    db: Session,
    school_id: int,
    student_id: int,
    class_id: Optional[int] = None,
    subject_id: Optional[int] = None
) -> List[Result]:
    query = db.query(Result).join(Assessment).filter(
        Assessment.school_id == school_id,
        Result.student_id == student_id
    )
    
    if class_id:
        query = query.filter(Assessment.class_id == class_id)
    if subject_id:
        query = query.filter(Assessment.subject_id == subject_id)
    
    return query.all()

def calculate_final_result(
    db: Session,
    school_id: int,
    student_id: int,
    class_id: int,
    subject_id: Optional[int] = None
) -> float:
    query = db.query(Result).join(Assessment).filter(
        Assessment.school_id == school_id,
        Result.student_id == student_id,
        Assessment.class_id == class_id
    )
    
    if subject_id:
        query = query.filter(Assessment.subject_id == subject_id)
    
    results = query.all()
    if not results:
        return 0.0
    
    total_weightage = 0
    weighted_sum = 0
    
    for result in results:
        assessment = result.assessment
        percentage = (result.marks_obtained / assessment.total_marks) * 100
        weighted_sum += percentage * assessment.weightage
        total_weightage += assessment.weightage
    
    return weighted_sum / total_weightage if total_weightage > 0 else 0.0

def create_teacher_note(
    db: Session,
    note_data: TeacherNoteCreate
) -> TeacherNote:
    note = TeacherNote(**note_data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_teacher_notes(
    db: Session,
    school_id: int,
    teacher_id: Optional[int] = None,
    class_id: Optional[int] = None,
    subject_id: Optional[int] = None
) -> List[TeacherNote]:
    query = db.query(TeacherNote).filter(TeacherNote.school_id == school_id)
    
    if teacher_id:
        query = query.filter(TeacherNote.teacher_id == teacher_id)
    if class_id:
        query = query.filter(TeacherNote.class_id == class_id)
    if subject_id:
        query = query.filter(TeacherNote.subject_id == subject_id)
    
    return query.all()