from datetime import datetime, timedelta, timezone, date
from src.services.appointment_service import create_appointment
from src.services.appointment_querey_service import list_appointments

class Dummy:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def model_dump(self):
        return self.__dict__

def test_list_appointments_by_date(db_session):
    data = Dummy(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc) + timedelta(hours=3),
        duration_minutes=30,
    )
    create_appointment(db_session, data)

    results = list_appointments(
        db_session,
        query_date=date.today(),
        doctor_id=1,
    )

    assert len(results) == 1
