from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from src.database import Base

class Appointment(Base):
    __tablename__ = "dheeraj_appointments"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("dheeraj_patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("dheeraj_doctors.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
