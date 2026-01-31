import pytest
from datetime import datetime, timedelta, timezone
from src.services.appointment_service import create_appointment

class Dummy:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def model_dump(self):
        return self.__dict__

def test_reject_past_appointment(db_session):
    data = Dummy(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc) - timedelta(minutes=10),
        duration_minutes=30,
    )
    with pytest.raises(ValueError):
        create_appointment(db_session, data)

def test_reject_invalid_duration(db_session):
    data = Dummy(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc) + timedelta(hours=1),
        duration_minutes=5,
    )
    with pytest.raises(ValueError):
        create_appointment(db_session, data)

def test_overlap_rejected(db_session):
    first = Dummy(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc) + timedelta(hours=1),
        duration_minutes=60,
    )
    create_appointment(db_session, first)

    second = Dummy(
        patient_id=1,
        doctor_id=1,
        start_time=first.start_time + timedelta(minutes=30),
        duration_minutes=30,
    )
    with pytest.raises(ValueError):
        create_appointment(db_session, second)

def test_create_valid_appointment(db_session):
    data = Dummy(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc) + timedelta(hours=2),
        duration_minutes=30,
    )
    appt = create_appointment(db_session, data)
    assert appt.id is not None
