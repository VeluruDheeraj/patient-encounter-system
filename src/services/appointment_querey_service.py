from sqlalchemy.orm import Session
from datetime import date, datetime, time
from src.models.appointment import Appointment


def list_appointments(db: Session, query_date: date, doctor_id: int | None):
    start = datetime.combine(query_date, time.min)
    end = datetime.combine(query_date, time.max)

    q = db.query(Appointment).filter(
        Appointment.start_time >= start,
        Appointment.start_time <= end,
    )

    if doctor_id:
        q = q.filter(Appointment.doctor_id == doctor_id)

    return q.all()
