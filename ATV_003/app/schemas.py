from pydantic import BaseModel
from typing import Optional

# Esquema Paciente
class PatientBase(BaseModel):
    name: str
    age: int
    address: str

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    class Config:
        orm_mode = True

# Esquema Médico
class DoctorBase(BaseModel):
    name: str
    specialty: str

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    class Config:
        orm_mode = True

# Esquema Consulta
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date: str
    description: Optional[str]

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: int
    class Config:
        orm_mode = True
