from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Medico, Usuario, TipoUsuario
from pydantic import BaseModel
from typing import List

router = APIRouter()

class MedicoCreate(BaseModel):
    nome: str
    email: str
    senha: str
    crm: str
    especialidade: str
    horario_atendimento: str

class MedicoSelect(BaseModel):
    id: int
    nome: str
    especialidade: str

    class Config:
        from_attributes = True

class MedicoList(BaseModel):
    id: int
    nome: str
    email: str
    crm: str
    especialidade: str
    horario_atendimento: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[MedicoList])
async def listar_medicos(db: Session = Depends(get_db)):
    """Lista todos os médicos."""
    medicos = db.query(Medico).join(Usuario).all()
    medicos_list = []
    for medico in medicos:
        medico_list = MedicoList(
            id=medico.id,
            nome=medico.usuario.nome,
            email=medico.usuario.email,
            crm=medico.crm,
            especialidade=medico.especialidade,
            horario_atendimento=medico.horario_atendimento
        )
        medicos_list.append(medico_list)
    return medicos_list

@router.post("/")
async def criar_medico(
    medico: MedicoCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo médico."""
    # Verifica se o email já está em uso
    if db.query(Usuario).filter(Usuario.email == medico.email).first():
        raise HTTPException(status_code=400, detail="Email já está em uso")

    # Verifica se o CRM já está em uso
    if db.query(Medico).filter(Medico.crm == medico.crm).first():
        raise HTTPException(status_code=400, detail="CRM já está em uso")

    # Cria o usuário
    usuario = Usuario(
        nome=medico.nome,
        email=medico.email,
        senha=medico.senha,
        tipo_usuario=TipoUsuario.MEDICO
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Cria o médico
    medico_db = Medico(
        usuario_id=usuario.id,
        crm=medico.crm,
        especialidade=medico.especialidade,
        horario_atendimento=medico.horario_atendimento
    )

    db.add(medico_db)
    db.commit()
    db.refresh(medico_db)

    return medico_db

@router.get("/{medico_id}")
async def obter_medico(medico_id: int, db: Session = Depends(get_db)):
    """Obtém um médico pelo ID."""
    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return medico

@router.put("/{medico_id}")
async def atualizar_medico(
    medico_id: int,
    especialidade: str = None,
    horario_atendimento: str = None,
    db: Session = Depends(get_db)
):
    """Atualiza um médico."""
    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    if especialidade:
        medico.especialidade = especialidade
    if horario_atendimento:
        medico.horario_atendimento = horario_atendimento

    db.commit()
    db.refresh(medico)
    return medico

@router.delete("/{medico_id}")
async def deletar_medico(medico_id: int, db: Session = Depends(get_db)):
    """Deleta um médico."""
    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    # Deleta o usuário associado
    usuario = db.query(Usuario).filter(Usuario.id == medico.usuario_id).first()
    if usuario:
        db.delete(usuario)

    db.delete(medico)
    db.commit()
    return {"message": "Médico deletado com sucesso"}

@router.get("/select", response_model=List[MedicoSelect])
async def listar_medicos_select(db: Session = Depends(get_db)):
    """Lista médicos em formato simplificado para select."""
    medicos = db.query(Medico).join(Usuario).all()
    medicos_select = []
    for medico in medicos:
        medico_select = MedicoSelect(
            id=medico.id,
            nome=medico.usuario.nome,
            especialidade=medico.especialidade
        )
        medicos_select.append(medico_select)
    return medicos_select
