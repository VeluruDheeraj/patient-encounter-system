from pydantic import BaseModel
from datetime import datetime


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    start_time: datetime
    duration_minutes: int


class AppointmentRead(AppointmentCreate):
    id: int
