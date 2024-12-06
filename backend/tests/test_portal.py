from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_get_student_dashboard(
    client: TestClient,
    student_token: str
):
    response = client.get(
        "/api/v1/student/dashboard",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "attendance" in data
    assert "assignments" in data
    assert "fees" in data
    assert "academics" in data

def test_get_student_assignments(
    client: TestClient,
    student_token: str
):
    response = client.get(
        "/api/v1/student/assignments",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "pending" in data
    assert "submitted" in data
    assert "graded" in data

def test_submit_assignment(
    client: TestClient,
    student_token: str
):
    # Create a test file
    files = {
        "file": ("test.pdf", b"test content", "application/pdf")
    }
    response = client.post(
        "/api/v1/student/assignments/1/submit",
        headers={"Authorization": f"Bearer {student_token}"},
        files=files,
        data={"comments": "Test submission"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["file_url"] is not None
    assert data["comments"] == "Test submission"

def test_get_student_results(
    client: TestClient,
    student_token: str
):
    response = client.get(
        "/api/v1/student/results",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        result = data[0]
        assert "subject" in result
        assert "total_percentage" in result
        assert "grade" in result
        assert "class_average" in result