from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from src.models.appointment import Appointment
from src.models.doctor import Doctor


def make_utc(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def create_appointment(db: Session, data):
    new_start = make_utc(data.start_time)

    now = datetime.now(timezone.utc)
    if new_start <= now:
        raise ValueError("Appointment must be in the future")

    if not 15 <= data.duration_minutes <= 180:
        raise ValueError("Invalid duration")

    doctor = db.get(Doctor, data.doctor_id)
    if not doctor or not doctor.is_active:
        raise ValueError("Doctor unavailable")

    new_end = new_start + timedelta(minutes=data.duration_minutes)

    existing = (
        db.query(Appointment).filter(Appointment.doctor_id == data.doctor_id).all()
    )

    for appt in existing:
        existing_start = make_utc(appt.start_time)
        existing_end = existing_start + timedelta(minutes=appt.duration_minutes)

        if new_start < existing_end and new_end > existing_start:
            raise ValueError("Overlapping appointment")

    appointment = Appointment(
        patient_id=data.patient_id,
        doctor_id=data.doctor_id,
        start_time=new_start,
        duration_minutes=data.duration_minutes,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
