from pydantic import BaseModel

class DoctorCreate(BaseModel):
    full_name: str
    specialization: str
    is_active: bool = True

class DoctorRead(DoctorCreate):
    id: int
