import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.models.patient import Patient
from src.models.doctor import Doctor
from src.models.appointment import Appointment

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    patient = Patient(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        phone="1234567890",
    )

    doctor = Doctor(
        full_name="Dr Test",
        specialization="General",
        is_active=True,
    )

    session.add_all([patient, doctor])
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)
