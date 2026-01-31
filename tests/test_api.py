import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app, get_db
from src.database import Base
from src.models.patient import Patient
from src.models.doctor import Doctor

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    patient = Patient(
        first_name="Test",
        last_name="User",
        email="api_unique@test.com",
        phone="123",
    )

    doctor = Doctor(
        full_name="Dr API",
        specialization="General",
        is_active=True,
    )

    db.add_all([patient, doctor])
    db.commit()

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_patient(client):
    r = client.post(
        "/patients",
        json={
            "first_name": "A",
            "last_name": "B",
            "email": "x@y.com",
            "phone": "999",
        },
    )
    assert r.status_code == 201

def test_get_patient(client):
    r = client.get("/patients/1")
    assert r.status_code == 200

def test_create_doctor(client):
    r = client.post(
        "/doctors",
        json={
            "full_name": "Dr X",
            "specialization": "Cardio",
            "is_active": True,
        },
    )
    assert r.status_code == 201

def test_get_doctor(client):
    r = client.get("/doctors/1")
    assert r.status_code == 200

def test_create_appointment_success(client):
    r = client.post(
        "/appointments",
        json={
            "patient_id": 1,
            "doctor_id": 1,
            "start_time": "2030-01-01T10:00:00+00:00",
            "duration_minutes": 30,
        },
    )
    assert r.status_code == 201

def test_create_appointment_conflict(client):
    client.post(
        "/appointments",
        json={
            "patient_id": 1,
            "doctor_id": 1,
            "start_time": "2030-01-01T10:00:00+00:00",
            "duration_minutes": 60,
        },
    )

    r = client.post(
        "/appointments",
        json={
            "patient_id": 1,
            "doctor_id": 1,
            "start_time": "2030-01-01T10:30:00+00:00",
            "duration_minutes": 30,
        },
    )

    assert r.status_code == 409

def test_list_appointments(client):
    r = client.get("/appointments", params={"date": "2030-01-01"})
    assert r.status_code in (200, 422)
