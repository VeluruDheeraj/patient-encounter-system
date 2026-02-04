from pydantic import BaseModel, EmailStr


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None


class PatientRead(PatientCreate):
    id: int
