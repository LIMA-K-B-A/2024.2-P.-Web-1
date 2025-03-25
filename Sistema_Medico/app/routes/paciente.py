from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Paciente
from pydantic import BaseModel
from datetime import date
from typing import Optional, List

router = APIRouter()

class PacienteCreate(BaseModel):
    nome: str
    cpf: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    endereco: Optional[str] = None

class PacienteSelect(BaseModel):
    id: int
    nome: str
    cpf: str

    class Config:
        from_attributes = True

@router.get("/")
async def listar_pacientes(db: Session = Depends(get_db)):
    """Lista todos os pacientes."""
    return db.query(Paciente).all()

@router.post("/")
async def criar_paciente(
    paciente: PacienteCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo paciente."""
    # Verifica se o CPF já está em uso
    if db.query(Paciente).filter(Paciente.cpf == paciente.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já está em uso")

    # Cria o paciente
    paciente_db = Paciente(
        nome=paciente.nome,
        cpf=paciente.cpf,
        email=paciente.email,
        telefone=paciente.telefone,
        data_nascimento=paciente.data_nascimento,
        endereco=paciente.endereco
    )

    db.add(paciente_db)
    db.commit()
    db.refresh(paciente_db)

    return paciente_db

@router.get("/{paciente_id}")
async def obter_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Obtém um paciente pelo ID."""
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente

@router.put("/{paciente_id}")
async def atualizar_paciente(
    paciente_id: int,
    paciente: PacienteCreate,
    db: Session = Depends(get_db)
):
    """Atualiza um paciente."""
    paciente_db = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Atualiza os campos
    paciente_db.nome = paciente.nome
    paciente_db.cpf = paciente.cpf
    paciente_db.email = paciente.email
    paciente_db.telefone = paciente.telefone
    paciente_db.data_nascimento = paciente.data_nascimento
    paciente_db.endereco = paciente.endereco

    db.commit()
    db.refresh(paciente_db)
    return paciente_db

@router.delete("/{paciente_id}")
async def deletar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Deleta um paciente."""
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    db.delete(paciente)
    db.commit()
    return {"message": "Paciente deletado com sucesso"}

@router.get("/select", response_model=List[PacienteSelect])
async def listar_pacientes_select(db: Session = Depends(get_db)):
    """Lista pacientes em formato simplificado para select."""
    pacientes = db.query(Paciente).all()
    pacientes_select = []
    for paciente in pacientes:
        paciente_select = PacienteSelect(
            id=paciente.id,
            nome=paciente.nome,
            cpf=paciente.cpf
        )
        pacientes_select.append(paciente_select)
    return pacientes_select
