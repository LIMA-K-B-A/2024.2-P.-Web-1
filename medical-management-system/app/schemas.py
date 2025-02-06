from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class PatientCreate(BaseModel):
    name: str
    age: int
    condition: str

class DoctorCreate(BaseModel):
    name: str
    specialty: str
    years_experience: int

class AppointmentCreate(BaseModel):
    date: datetime
    patient_id: int
    doctor_id: int
    notes: str