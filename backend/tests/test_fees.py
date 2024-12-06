from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.fee import (
    FeeStructure,
    FeeType,
    PaymentInterval,
    PaymentStatus
)

def test_create_fee_structure(
    client: TestClient,
    schooladmin_token: str
):
    response = client.post(
        "/api/v1/fees",
        headers={"Authorization": f"Bearer {schooladmin_token}"},
        json={
            "school_id": 1,
            "name": "Test Fee",
            "fee_type": FeeType.TUITION,
            "amount": 5000.00,
            "interval": PaymentInterval.MONTHLY,
            "class_id": 1,
            "academic_year": "2024"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Fee"
    assert data["amount"] == 5000.00

def test_create_fee_discount(
    client: TestClient,
    schooladmin_token: str,
    test_users: dict
):
    response = client.post(
        "/api/v1/fees/discounts",
        headers={"Authorization": f"Bearer {schooladmin_token}"},
        json={
            "fee_structure_id": 1,
            "student_id": test_users["student"].id,
            "amount": 500.00,
            "reason": "Sibling discount"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 500.00
    assert data["reason"] == "Sibling discount"

def test_record_fee_payment(
    client: TestClient,
    schooladmin_token: str,
    test_users: dict
):
    response = client.post(
        "/api/v1/fees/pay",
        headers={"Authorization": f"Bearer {schooladmin_token}"},
        json={
            "fee_structure_id": 1,
            "student_id": test_users["student"].id,
            "amount_paid": 4500.00,
            "payment_method": "bank_transfer",
            "remarks": "Monthly fee payment"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount_paid"] == 4500.00
    assert data["status"] == PaymentStatus.PAID

def test_get_fee_report(
    client: TestClient,
    schooladmin_token: str
):
    response = client.post(
        "/api/v1/fees/report",
        headers={"Authorization": f"Bearer {schooladmin_token}"},
        json={
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "fee_type": FeeType.TUITION
        }
    )
    assert response.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in response.headers["content-type"]