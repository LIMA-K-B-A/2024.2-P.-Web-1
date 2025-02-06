from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class PatientBase(BaseModel):
    name: str
    age: int
    gender: str

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int

    class Config:
        orm_mode = True

class DoctorBase(BaseModel):
    name: str
    specialization: str

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int

    class Config:
        orm_mode = True

class AppointmentBase(BaseModel):
    date: str
    patient_id: int
    doctor_id: int

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
