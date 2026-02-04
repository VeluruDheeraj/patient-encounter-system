from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from src.database import SessionLocal
from src.schemas.patient import PatientCreate, PatientRead
from src.schemas.doctor import DoctorCreate, DoctorRead
from src.schemas.appointment import AppointmentCreate, AppointmentRead
from src.services.patient_service import create_patient, get_patient
from src.services.doctor_service import create_doctor, get_doctor
from src.services.appointment_service import create_appointment
from src.services.appointment_querey_service import list_appointments

app = FastAPI(
    title="Medical Encounter Management System",
    version="1.0.0",
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/patients", response_model=PatientRead, status_code=201)
def create_patient_api(data: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db, data)

@app.get("/patients/{patient_id}", response_model=PatientRead)
def get_patient_api(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/doctors", response_model=DoctorRead, status_code=201)
def create_doctor_api(data: DoctorCreate, db: Session = Depends(get_db)):
    return create_doctor(db, data)

@app.get("/doctors/{doctor_id}", response_model=DoctorRead)
def get_doctor_api(doctor_id: int, db: Session = Depends(get_db)):
    doctor = get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.post("/appointments", response_model=AppointmentRead, status_code=201)
def schedule_appointment_api(data: AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return create_appointment(db, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.get("/appointments", response_model=List[AppointmentRead])
def list_appointments_api(date: date, doctor_id: int | None = None, db: Session = Depends(get_db)):
    return list_appointments(db, date, doctor_id)
