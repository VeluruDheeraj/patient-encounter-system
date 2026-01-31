from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from src.models.appointment import Appointment

def list_appointments(
    db: Session,
    query_date,
    doctor_id: int | None = None,
):
    start = datetime.combine(query_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    end = start + timedelta(days=1)

    q = db.query(Appointment).filter(
        Appointment.start_time >= start,
        Appointment.start_time < end,
    )

    if doctor_id is not None:
        q = q.filter(Appointment.doctor_id == doctor_id)

    return q.all()
