from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.academic import (
    Timetable,
    Assessment,
    WeekDay,
    AssessmentType
)
from datetime import datetime

def test_create_timetable(
    client: TestClient,
    teacher_token: str,
    test_users: dict,
    test_tenant: dict
):
    response = client.post(
        "/api/v1/academic/timetable",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "school_id": 1,
            "class_id": 1,
            "subject_id": 1,
            "teacher_id": test_users["teacher"].id,
            "day": WeekDay.MONDAY,
            "start_time": "09:00:00",
            "end_time": "10:00:00",
            "room": "101"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["teacher_id"] == test_users["teacher"].id
    assert data["day"] == WeekDay.MONDAY

def test_create_assessment(
    client: TestClient,
    teacher_token: str,
    test_users: dict
):
    response = client.post(
        "/api/v1/academic/assessments",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "school_id": 1,
            "class_id": 1,
            "subject_id": 1,
            "teacher_id": test_users["teacher"].id,
            "grading_system_id": 1,
            "name": "Test Assessment",
            "type": AssessmentType.TEST,
            "total_marks": 100,
            "weightage": 20,
            "description": "Test description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Assessment"
    assert data["total_marks"] == 100

def test_get_timetable(
    client: TestClient,
    student_token: str
):
    response = client.get(
        "/api/v1/academic/timetable",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_student_results(
    client: TestClient,
    student_token: str,
    test_users: dict
):
    response = client.get(
        f"/api/v1/academic/results/student/{test_users['student'].id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)