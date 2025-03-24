from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class TipoUsuario(str, enum.Enum):
    ADMIN = "admin"
    MEDICO = "medico"
    PACIENTE = "paciente"

class StatusConsulta(str, enum.Enum):
    AGENDADA = "agendada"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    REALIZADA = "realizada"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    tipo_usuario = Column(SQLEnum(TipoUsuario), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    medico = relationship("Medico", back_populates="usuario", uselist=False)

    class Config:
        from_attributes = True

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    crm = Column(String(20), unique=True, nullable=False)
    especialidade = Column(String(100), nullable=False)
    horario_atendimento = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    usuario = relationship("Usuario", back_populates="medico")
    consultas = relationship("Consulta", back_populates="medico")

    class Config:
        from_attributes = True

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    email = Column(String(100))
    telefone = Column(String(20))
    data_nascimento = Column(DateTime(timezone=True))
    endereco = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    consultas = relationship("Consulta", back_populates="paciente")

    class Config:
        from_attributes = True

class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    medico_id = Column(Integer, ForeignKey("medicos.id"))
    data_hora = Column(DateTime(timezone=True), nullable=False)
    tipo_consulta = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)
    observacoes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")

    class Config:
        from_attributes = True
