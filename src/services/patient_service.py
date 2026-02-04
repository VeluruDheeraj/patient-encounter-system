from sqlalchemy.orm import Session
from src.models.patient import Patient


def create_patient(db: Session, data):
    patient = Patient(**data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patient(db: Session, patient_id: int):
    return db.get(Patient, patient_id)
