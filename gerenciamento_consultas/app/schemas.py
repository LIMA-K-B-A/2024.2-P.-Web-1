from pydantic import BaseModel

# Modelo Pydantic para Patient
class PatientBase(BaseModel):
    name: str
    age: int
    condition: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True

# Modelo Pydantic para Doctor
class DoctorBase(BaseModel):
    name: str
    specialty: str
    years_of_experience: int

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int

    class Config:
        from_attributes = True

# Modelo Pydantic para Appointment
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date: str
    time: str

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int

    class Config:
        from_attributes = True