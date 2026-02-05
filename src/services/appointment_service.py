from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from src.models.appointment import Appointment
from src.models.doctor import Doctor


def _make_utc(dt):
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")
    return dt.astimezone(timezone.utc)


def _ensure_future(start_time: datetime):
    now = datetime.now(timezone.utc)
    if start_time <= now:
        raise ValueError("Appointment must be in the future")


def _ensure_valid_duration(duration: int):
    if not 15 <= duration <= 180:
        raise ValueError("Invalid duration")


def _ensure_doctor_available(db: Session, doctor_id: int):
    doctor = db.get(Doctor, doctor_id)
    if not doctor or not doctor.is_active:
        raise ValueError("Doctor unavailable")


def _has_overlap(db: Session, doctor_id: int, new_start: datetime, duration: int):
    new_end = new_start + timedelta(minutes=duration)

    existing = db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()

    for appt in existing:
        existing_start = _make_utc(appt.start_time)
        existing_end = existing_start + timedelta(minutes=appt.duration_minutes)

        if new_start < existing_end and new_end > existing_start:
            return True

    return False


def create_appointment(db: Session, data):
    new_start = _make_utc(data.start_time)

    _ensure_future(new_start)
    _ensure_valid_duration(data.duration_minutes)
    _ensure_doctor_available(db, data.doctor_id)

    if _has_overlap(
        db,
        data.doctor_id,
        new_start,
        data.duration_minutes,
    ):
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
