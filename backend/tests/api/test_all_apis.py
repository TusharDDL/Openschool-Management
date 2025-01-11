import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from app.main import app
from app.core.config import get_settings
from tests.utils.utils import random_email, random_lower_string

settings = get_settings()
client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.fixture(scope="session")
def auth_token():
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "Admin123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    return data["access_token"]

class TestAuthentication:
    def test_login_saas_admin(self):
        response = client.post("/api/v1/auth/login", json={
            "email": "admin@example.com",
            "password": "Admin123!"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_get_current_user(self):
        # Get a fresh token
        response = client.post("/api/v1/auth/login", json={
            "email": "admin@example.com",
            "password": "Admin123!"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        token = data["access_token"]

        # Use the token to get current user info
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "admin@example.com"
        assert data["role"] == "SUPER_ADMIN"
        assert data["is_saas_admin"] is True

    def test_invalid_login(self):
        response = client.post("/api/v1/auth/login", json={
            "email": "wrong@example.com",
            "password": "wrong"
        })
        assert response.status_code == 401

@pytest.fixture(scope="session")
def tenant_id(auth_token):
    response = client.post(
        "/api/v1/tenants",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"name": "Test Tenant"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Tenant"
    return data["id"]

class TestTenantManagement:

    def test_create_tenant(self, auth_token):
        response = client.post(
            "/api/v1/tenants",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"name": "Another Test Tenant"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Another Test Tenant"

    def test_get_tenant(self, auth_token, tenant_id):
        response = client.get(
            f"/api/v1/tenants/{tenant_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == tenant_id

    def test_list_tenants(self, auth_token):
        response = client.get(
            "/api/v1/tenants",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

@pytest.fixture(scope="session")
def school_id(auth_token, tenant_id):
    response = client.post(
        "/api/v1/schools",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "tenant_id": tenant_id,
            "name": "Test School",
            "address": "123 Test St",
            "phone": "1234567890"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test School"
    return data["id"]

class TestSchoolManagement:

    def test_create_school(self, auth_token, tenant_id):
        response = client.post(
            "/api/v1/schools",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "tenant_id": tenant_id,
                "name": "Another Test School",
                "address": "456 Test St",
                "phone": "9876543210"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Another Test School"

    def test_get_school(self, auth_token, school_id):
        response = client.get(
            f"/api/v1/schools/{school_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == school_id

@pytest.fixture(scope="session")
def academic_year_id(auth_token, tenant_id, school_id):
    response = client.post(
        "/api/v1/academic/years",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "tenant_id": tenant_id,
            "school_id": school_id,
            "name": "2024-2025",
            "start_date": "2024-06-01",
            "end_date": "2025-05-31",
            "is_active": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "2024-2025"
    return data["id"]

@pytest.fixture(scope="session")
def class_id(auth_token, tenant_id, school_id, academic_year_id):
    response = client.post(
        "/api/v1/academic/classes",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "tenant_id": tenant_id,
            "school_id": school_id,
            "academic_year_id": academic_year_id,
            "name": "Class 10A",
            "grade_level": 10
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Class 10A"
    return data["id"]

@pytest.fixture(scope="session")
def subject_id(auth_token, tenant_id, school_id):
    response = client.post(
        "/api/v1/academic/subjects",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "tenant_id": tenant_id,
            "school_id": school_id,
            "name": "Mathematics",
            "code": "MATH101",
            "credits": 5
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Mathematics"
    return data["id"]

class TestAcademicManagement:

    def test_create_academic_year(self, auth_token, tenant_id, school_id):
        response = client.post(
            "/api/v1/academic/years",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "tenant_id": tenant_id,
                "school_id": school_id,
                "name": "2025-2026",
                "start_date": "2025-06-01",
                "end_date": "2026-05-31",
                "is_active": True
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "2025-2026"

    def test_create_class(self, auth_token, tenant_id, school_id, academic_year_id):
        response = client.post(
            "/api/v1/academic/classes",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "tenant_id": tenant_id,
                "school_id": school_id,
                "academic_year_id": academic_year_id,
                "name": "Class 10B",
                "grade_level": 10
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Class 10B"

    def test_create_subject(self, auth_token, tenant_id, school_id):
        response = client.post(
            "/api/v1/academic/subjects",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "tenant_id": tenant_id,
                "school_id": school_id,
                "name": "Physics",
                "code": "PHY101",
                "credits": 5
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Physics"

@pytest.fixture(scope="session")
def timetable_id(auth_token, tenant_id, school_id, academic_year_id):
    response = client.post(
        "/api/v1/academic/timetables",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "tenant_id": tenant_id,
            "school_id": school_id,
            "academic_year_id": academic_year_id,
            "name": "Regular Timetable",
            "effective_from": "2024-06-01",
            "is_active": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Regular Timetable"
    return data["id"]

@pytest.fixture(scope="session")
def period_id(auth_token, tenant_id, timetable_id):
    response = client.post(
        f"/api/v1/academic/timetables/{timetable_id}/periods",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "tenant_id": tenant_id,
            "timetable_id": timetable_id,
            "period_number": 1,
            "name": "First Period",
            "start_time": "08:00",
            "end_time": "09:00",
            "day": "MONDAY"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "First Period"
    return data["id"]

class TestTimetableManagement:

    def test_create_timetable(self, auth_token, tenant_id, school_id, academic_year_id):
        response = client.post(
            "/api/v1/academic/timetables",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "tenant_id": tenant_id,
                "school_id": school_id,
                "academic_year_id": academic_year_id,
                "name": "Special Timetable",
                "effective_from": "2024-06-01",
                "is_active": True
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Special Timetable"

    def test_add_period(self, auth_token, tenant_id, timetable_id):
        response = client.post(
            f"/api/v1/academic/timetables/{timetable_id}/periods",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "tenant_id": tenant_id,
                "timetable_id": timetable_id,
                "period_number": 2,
                "name": "Second Period",
                "start_time": "09:00",
                "end_time": "10:00",
                "day": "MONDAY"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Second Period"

@pytest.fixture(scope="session")
def student_id(auth_token, school_id):
    response = client.post(
        "/api/v1/students",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "school_id": school_id,
            "first_name": "John",
            "last_name": "Doe",
            "admission_number": "2024001",
            "admission_date": "2024-06-01",
            "date_of_birth": "2010-01-01",
            "gender": "MALE",
            "email": "john.doe@example.com",
            "phone": "1234567890"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    return data["id"]

class TestStudentManagement:

    def test_create_student(self, auth_token, school_id):
        response = client.post(
            "/api/v1/students",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "school_id": school_id,
                "first_name": "Jane",
                "last_name": "Smith",
                "admission_number": "2024002",
                "admission_date": "2024-06-01",
                "date_of_birth": "2010-02-01",
                "gender": "FEMALE",
                "email": "jane.smith@example.com",
                "phone": "9876543210"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["first_name"] == "Jane"

    def test_add_guardian(self, auth_token, student_id):
        response = client.post(
            f"/api/v1/students/{student_id}/guardians",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "relation_type": "FATHER",
                "first_name": "James",
                "last_name": "Doe",
                "phone": "9876543210",
                "email": "james.doe@example.com"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["first_name"] == "James"

class TestAttendanceManagement:
    def test_mark_attendance(self, auth_token, student_id):
        response = client.post(
            "/api/v1/attendance",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "student_id": student_id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": "PRESENT"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "PRESENT"

    def test_get_attendance_report(self, auth_token, student_id):
        response = client.get(
            f"/api/v1/attendance/student/{student_id}/report",
            headers={"Authorization": f"Bearer {auth_token}"},
            params={
                "start_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                "end_date": datetime.now().strftime("%Y-%m-%d")
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "attendance_percentage" in data

@pytest.fixture(scope="session")
def exam_id(auth_token, academic_year_id):
    response = client.post(
        "/api/v1/exams",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "academic_year_id": academic_year_id,
            "name": "Mid Term Exam",
            "exam_type": "MID_TERM",
            "start_date": "2024-09-01",
            "end_date": "2024-09-10",
            "grade_scale": "PERCENTAGE",
            "passing_percentage": 35
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Mid Term Exam"
    return data["id"]

class TestExamManagement:

    def test_create_exam(self, auth_token, academic_year_id):
        response = client.post(
            "/api/v1/exams",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "academic_year_id": academic_year_id,
                "name": "Final Exam",
                "exam_type": "FINAL",
                "start_date": "2024-12-01",
                "end_date": "2024-12-10",
                "grade_scale": "PERCENTAGE",
                "passing_percentage": 35
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Final Exam"

    def test_add_exam_subject(self, auth_token, exam_id, subject_id):
        response = client.post(
            f"/api/v1/exams/{exam_id}/subjects",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "subject_id": subject_id,
                "max_marks": 100,
                "passing_marks": 35,
                "exam_date": "2024-09-01",
                "start_time": "09:00",
                "duration": 180
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["max_marks"] == 100

@pytest.fixture(scope="session")
def fee_structure_id(auth_token, academic_year_id):
    response = client.post(
        "/api/v1/fee-structures",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "academic_year_id": academic_year_id,
            "name": "Tuition Fee",
            "fee_type": "TUITION",
            "amount": 50000,
            "payment_interval": "QUARTERLY"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Tuition Fee"
    return data["id"]

class TestFeeManagement:

    def test_create_fee_structure(self, auth_token, academic_year_id):
        response = client.post(
            "/api/v1/fee-structures",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "academic_year_id": academic_year_id,
                "name": "Library Fee",
                "fee_type": "LIBRARY",
                "amount": 5000,
                "payment_interval": "ANNUAL"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Library Fee"

    def test_create_fee_item(self, auth_token, fee_structure_id, student_id):
        response = client.post(
            "/api/v1/fee-items",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "fee_structure_id": fee_structure_id,
                "student_id": student_id,
                "amount": 12500,
                "due_date": "2024-07-01"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["amount"] == 12500

@pytest.fixture(scope="session")
def resource_id(auth_token, school_id):
    response = client.post(
        "/api/v1/resources",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "school_id": school_id,
            "name": "Physics Lab",
            "code": "LAB001",
            "resource_type": "LAB",
            "capacity": 30
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Physics Lab"
    return data["id"]

class TestResourceManagement:

    def test_create_resource(self, auth_token, school_id):
        response = client.post(
            "/api/v1/resources",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "school_id": school_id,
                "name": "Chemistry Lab",
                "code": "LAB002",
                "resource_type": "LAB",
                "capacity": 30
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Chemistry Lab"

    def test_book_resource(self, auth_token, resource_id):
        response = client.post(
            "/api/v1/resource-bookings",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "resource_id": resource_id,
                "start_time": "2024-06-01T09:00:00",
                "end_time": "2024-06-01T11:00:00",
                "purpose": "Physics Practical"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "CONFIRMED"

@pytest.fixture(scope="session")
def calendar_id(auth_token, school_id):
    response = client.post(
        "/api/v1/calendars",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "school_id": school_id,
            "name": "Academic Calendar",
            "is_public": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Academic Calendar"
    return data["id"]

class TestCalendarManagement:

    def test_create_calendar(self, auth_token, school_id):
        response = client.post(
            "/api/v1/calendars",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "school_id": school_id,
                "name": "Sports Calendar",
                "is_public": True
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Sports Calendar"

    def test_create_event(self, auth_token, calendar_id):
        response = client.post(
            "/api/v1/events",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "calendar_id": calendar_id,
                "title": "Annual Day",
                "event_type": "CULTURAL",
                "start_time": "2024-12-20T16:00:00",
                "end_time": "2024-12-20T20:00:00",
                "location": "School Auditorium"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Annual Day"

@pytest.fixture(scope="session")
def staff_id(auth_token, school_id):
    response = client.post(
        "/api/v1/staff",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "school_id": school_id,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "9876543210",
            "employee_id": "EMP001",
            "designation": "Teacher",
            "employment_type": "FULL_TIME",
            "join_date": "2024-06-01"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Jane"
    return data["id"]

class TestStaffManagement:

    def test_create_staff(self, auth_token, school_id):
        response = client.post(
            "/api/v1/staff",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "school_id": school_id,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
                "employee_id": "EMP002",
                "designation": "Teacher",
                "employment_type": "FULL_TIME",
                "join_date": "2024-06-01"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["first_name"] == "John"

    def test_apply_leave(self, auth_token, staff_id):
        response = client.post(
            "/api/v1/staff-leaves",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "staff_id": staff_id,
                "leave_type": "CASUAL",
                "start_date": "2024-07-01",
                "end_date": "2024-07-02",
                "reason": "Personal work"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "PENDING"

@pytest.fixture(scope="session")
def dashboard_id(auth_token):
    response = client.post(
        "/api/v1/dashboards",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "name": "Academic Overview",
            "description": "Overview of academic performance",
            "layout": {
                "widgets": [
                    {
                        "id": "attendance_chart",
                        "type": "CHART",
                        "position": {"x": 0, "y": 0, "w": 6, "h": 4}
                    }
                ]
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Academic Overview"
    return data["id"]

class TestAnalytics:

    def test_create_dashboard(self, auth_token):
        response = client.post(
            "/api/v1/dashboards",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "name": "Financial Overview",
                "description": "Overview of financial performance",
                "layout": {
                    "widgets": [
                        {
                            "id": "fee_collection_chart",
                            "type": "CHART",
                            "position": {"x": 0, "y": 0, "w": 6, "h": 4}
                        }
                    ]
                }
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Financial Overview"

    def test_create_widget(self, auth_token, dashboard_id):
        response = client.post(
            f"/api/v1/dashboards/{dashboard_id}/widgets",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "title": "Attendance Trend",
                "widget_type": "CHART",
                "chart_type": "LINE",
                "query": "SELECT date, COUNT(*) as present_count FROM attendance WHERE status = 'PRESENT' GROUP BY date",
                "refresh_interval": 3600
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Attendance Trend"

def test_all():
    # Run authentication tests
    auth = TestAuthentication()
    auth.test_login_saas_admin()
    auth.test_get_current_user()
    auth.test_invalid_login()

    # Run tenant tests
    tenant = TestTenantManagement()
    tenant.test_create_tenant(auth_token)
    tenant.test_get_tenant(auth_token, tenant_id)
    tenant.test_list_tenants(auth_token)

    # Run school tests
    school = TestSchoolManagement()
    school.test_create_school(auth_token, tenant_id)
    school.test_get_school(auth_token, school_id)

    # Run academic tests
    academic = TestAcademicManagement()
    academic.test_create_academic_year(auth_token, school_id)
    academic.test_create_class(auth_token, school_id, academic_year_id)
    academic.test_create_subject(auth_token, school_id)

    # Run timetable tests
    timetable = TestTimetableManagement()
    timetable.test_create_timetable(auth_token, academic_year_id)
    timetable.test_add_period(auth_token, timetable_id)

    # Run student tests
    student = TestStudentManagement()
    student.test_create_student(auth_token, school_id)
    student.test_add_guardian(auth_token, student_id)

    # Run attendance tests
    attendance = TestAttendanceManagement()
    attendance.test_mark_attendance(auth_token, student_id)
    attendance.test_get_attendance_report(auth_token, student_id)

    # Run exam tests
    exam = TestExamManagement()
    exam.test_create_exam(auth_token, academic_year_id)
    exam.test_add_exam_subject(auth_token, exam_id, subject_id)

    # Run fee tests
    fee = TestFeeManagement()
    fee.test_create_fee_structure(auth_token, academic_year_id)
    fee.test_create_fee_item(auth_token, fee_structure_id, student_id)

    # Run resource tests
    resource = TestResourceManagement()
    resource.test_create_resource(auth_token, school_id)
    resource.test_book_resource(auth_token, resource_id)

    # Run calendar tests
    calendar = TestCalendarManagement()
    calendar.test_create_calendar(auth_token, school_id)
    calendar.test_create_event(auth_token, calendar_id)

    # Run staff tests
    staff = TestStaffManagement()
    staff.test_create_staff(auth_token, school_id)
    staff.test_apply_leave(auth_token, staff_id)

    # Run analytics tests
    analytics = TestAnalytics()
    analytics.test_create_dashboard(auth_token)
    analytics.test_create_widget(auth_token, dashboard_id)

if __name__ == "__main__":
    test_all()