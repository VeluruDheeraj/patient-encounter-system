from src.services.doctor_service import create_doctor, get_doctor

class Dummy:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def model_dump(self):
        return self.__dict__

def test_create_and_get_doctor(db_session):
    data = Dummy(
        full_name="Dr X",
        specialization="Cardiology",
        is_active=True,
    )
    doctor = create_doctor(db_session, data)
    fetched = get_doctor(db_session, doctor.id)
    assert fetched.full_name == "Dr X"
