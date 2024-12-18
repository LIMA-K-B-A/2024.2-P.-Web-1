# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MedicoBase(BaseModel):
    nome: str
    especializacao: str
    crm: str

class MedicoCreate(MedicoBase):
    pass

class MedicoUpdate(MedicoBase):
    nome: Optional[str] = None
    especializacao: Optional[str] = None
    crm: Optional[str] = None

class Medico(MedicoBase):
    id: int

    class Config:
        orm_mode = True

class PacienteBase(BaseModel):
    nome: str
    idade: int
    cpf: str
    telefone: str

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(PacienteBase):
    nome: Optional[str] = None
    idade: Optional[int] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None

class Paciente(PacienteBase):
    id: int

    class Config:
        orm_mode = True

class ConsultaBase(BaseModel):
    paciente_id: int
    medico_id: int
    data_consulta: datetime

class ConsultaCreate(ConsultaBase):
    pass

class ConsultaUpdate(ConsultaBase):
    paciente_id: Optional[int] = None
    medico_id: Optional[int] = None
    data_consulta: Optional[datetime] = None

class Consulta(ConsultaBase):
    id: int

    class Config:
        orm_mode = True
