from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from passlib.context import CryptContext  # Para hashing de senhas
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Para criptografar a senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo SQLAlchemy User
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # Se você usa 'hashed_password' ao invés de 'password'
    role = Column(String)
    
    def __init__(self, email, hashed_password, role):
        self.email = email
        self.hashed_password = hashed_password  # Certifique-se de que 'hashed_password' está sendo usado
        self.role = role

# Pydantic models para resposta e criação de usuário
class UserResponse(BaseModel):
    email: EmailStr
    role: str

    class Config:
        from_attributes = True  # Permite que o Pydantic converta objetos SQLAlchemy em modelos Pydantic

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str  # Adicionando a role como necessário

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

# Modelo para Token (para autenticação)
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

# Base para paciente, médico e consulta
class PatientBase(BaseModel):
    name: str
    age: int
    condition: str

class DoctorBase(BaseModel):
    name: str
    specialty: str
    years_experience: int

class AppointmentBase(BaseModel):
    date: datetime
    patient_id: int
    doctor_id: int
    notes: Optional[str] = None

# Pydantic models para criação
class PatientCreate(PatientBase):
    pass

class DoctorCreate(DoctorBase):
    pass

class AppointmentCreate(AppointmentBase):
    pass

# Pydantic models para leitura e retorno (inclui id)
class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True  # Isso permite que o Pydantic converta objetos ORM para modelos Pydantic

class Doctor(DoctorBase):
    id: int

    class Config:
        from_attributes = True

class Appointment(AppointmentBase):
    id: int
    patient: Patient  # Relacionamento com o paciente
    doctor: Doctor  # Relacionamento com o médico

    class Config:
        from_attributes = True  # Isso permite que o Pydantic converta objetos ORM para modelos Pydantic

# Para retorno de listas (para consultas)
class AppointmentList(BaseModel):
    appointments: List[Appointment]

    class Config:
        from_attributes = True
