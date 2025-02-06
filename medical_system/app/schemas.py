from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    email: str
    full_name: str
    photo: str

    class Config:
        orm_mode = True

class DoctorCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    specialty: str

class PatientCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    birth_date: datetime

class AppointmentCreate(BaseModel):
    appointment_time: datetime
    reason: str

class UserUpdate(BaseModel):
    email: str
    full_name: str
    password: str

class DoctorUpdate(BaseModel):
    full_name: str
    email: str
    phone: str
    specialty: str

class PatientUpdate(BaseModel):
    full_name: str
    email: str
    phone: str
    birth_date: datetime

class AppointmentUpdate(BaseModel):
    appointment_time: datetime
    reason: str
