from src.services.patient_service import create_patient, get_patient

class Dummy:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def model_dump(self):
        return self.__dict__

def test_create_and_get_patient(db_session):
    data = Dummy(
        first_name="A",
        last_name="B",
        email="a@b.com",
        phone="9999999999",
    )
    patient = create_patient(db_session, data)
    fetched = get_patient(db_session, patient.id)
    assert fetched.email == "a@b.com"
