from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import time, date, datetime
from fastapi import UploadFile, File
from app.models import TipoUsuario, StatusConsulta
from enum import Enum

# -------- Paciente --------
class PacienteBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    cpf: str = Field(..., min_length=11, max_length=14)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    endereco: Optional[str] = None

    class Config:
        from_attributes = True

class PacienteCreate(PacienteBase):
    pass

class PacienteOut(PacienteBase):
    id: int
    created_at: datetime
    updated_at: datetime


class PacienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    cpf: Optional[str] = Field(None, min_length=11, max_length=14)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    endereco: Optional[str] = None


# -------- Médico --------
class MedicoBase(BaseModel):
    crm: str = Field(..., min_length=4, max_length=20)
    especialidade: str
    horario_atendimento: str

    class Config:
        from_attributes = True

class MedicoCreate(MedicoBase):
    usuario_id: int

class MedicoOut(MedicoBase):
    id: int
    usuario_id: int
    created_at: datetime
    updated_at: datetime


class MedicoUpdate(BaseModel):
    crm: Optional[str] = Field(None, min_length=4, max_length=20)
    especialidade: Optional[str] = None
    horario_atendimento: Optional[str] = None


# -------- Consulta --------
class ConsultaBase(BaseModel):
    paciente_id: int
    medico_id: int
    data_hora: datetime
    tipo_consulta: str
    status: str
    observacoes: Optional[str] = None

    class Config:
        from_attributes = True

class ConsultaCreate(ConsultaBase):
    pass

class ConsultaOut(ConsultaBase):
    id: int
    created_at: datetime
    updated_at: datetime


# -------- Usuário --------
class TipoUsuario(str, Enum):
    PACIENTE = "PACIENTE"
    MEDICO = "MEDICO"
    ADMIN = "ADMIN"

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    tipo_usuario: TipoUsuario

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    tipo_usuario: Optional[TipoUsuario] = None

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


# -------- Resposta de Erro --------
class ErrorResponse(BaseModel):
    detail: str
