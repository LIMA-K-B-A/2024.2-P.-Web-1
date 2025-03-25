from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Paciente, Usuario, TipoUsuario
from pydantic import BaseModel
from datetime import date
from typing import List

router = APIRouter()

class PacienteCreate(BaseModel):
    nome: str
    email: str
    senha: str
    cpf: str
    data_nascimento: date
    telefone: str

class PacienteList(BaseModel):
    id: int
    nome: str
    email: str
    cpf: str
    data_nascimento: date
    telefone: str

    class Config:
        from_attributes = True

class PacienteSelect(BaseModel):
    id: int
    nome: str
    cpf: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[PacienteList])
async def listar_pacientes(db: Session = Depends(get_db)):
    """Lista todos os pacientes."""
    pacientes = db.query(Paciente).join(Paciente.usuario).all()
    pacientes_list = []
    for paciente in pacientes:
        paciente_list = PacienteList(
            id=paciente.id,
            nome=paciente.usuario.nome,
            email=paciente.usuario.email,
            cpf=paciente.cpf,
            data_nascimento=paciente.data_nascimento,
            telefone=paciente.telefone
        )
        pacientes_list.append(paciente_list)
    return pacientes_list

@router.post("/")
async def criar_paciente(
    paciente: PacienteCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo paciente."""
    try:
        # Verifica se o email já está em uso
        if db.query(Usuario).filter(Usuario.email == paciente.email).first():
            raise HTTPException(status_code=400, detail="Email já está em uso")

        # Verifica se o CPF já está em uso
        if db.query(Paciente).filter(Paciente.cpf == paciente.cpf).first():
            raise HTTPException(status_code=400, detail="CPF já está em uso")

        # Cria o usuário primeiro
        usuario = Usuario(
            nome=paciente.nome,
            email=paciente.email,
            senha=paciente.senha,
            tipo_usuario=TipoUsuario.PACIENTE
        )
        db.add(usuario)
        db.flush()  # Garante que o ID do usuário seja gerado

        # Cria o paciente vinculado ao usuário
        paciente_db = Paciente(
            usuario_id=usuario.id,
            cpf=paciente.cpf,
            data_nascimento=paciente.data_nascimento,
            telefone=paciente.telefone
        )
        db.add(paciente_db)
        db.commit()
        db.refresh(paciente_db)
        db.refresh(usuario)

        # Retorna os dados combinados
        return {
            "id": paciente_db.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cpf": paciente_db.cpf,
            "data_nascimento": paciente_db.data_nascimento,
            "telefone": paciente_db.telefone
        }

    except Exception as e:
        db.rollback()
        # Converte o erro do PostgreSQL para uma mensagem mais amigável
        error_msg = str(e)
        if "violates not-null constraint" in error_msg:
            if "nome" in error_msg:
                error_msg = "O nome é obrigatório"
            elif "email" in error_msg:
                error_msg = "O email é obrigatório"
            elif "cpf" in error_msg:
                error_msg = "O CPF é obrigatório"
        raise HTTPException(status_code=400, detail=error_msg)

@router.get("/{paciente_id}")
async def obter_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Obtém um paciente pelo ID."""
    paciente = db.query(Paciente).join(Paciente.usuario).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return {
        "id": paciente.id,
        "nome": paciente.usuario.nome,
        "email": paciente.usuario.email,
        "cpf": paciente.cpf,
        "data_nascimento": paciente.data_nascimento,
        "telefone": paciente.telefone
    }

@router.delete("/{paciente_id}")
async def deletar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Deleta um paciente."""
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Deleta o usuário associado
    usuario = db.query(Usuario).filter(Usuario.id == paciente.usuario_id).first()
    if usuario:
        db.delete(usuario)

    db.delete(paciente)
    db.commit()
    return {"message": "Paciente deletado com sucesso"}

@router.get("/select", response_model=List[PacienteSelect])
async def listar_pacientes_select(db: Session = Depends(get_db)):
    """Lista pacientes em formato simplificado para select."""
    pacientes = db.query(Paciente).join(Paciente.usuario).all()
    pacientes_select = []
    for paciente in pacientes:
        paciente_select = PacienteSelect(
            id=paciente.id,
            nome=paciente.usuario.nome,
            cpf=paciente.cpf
        )
        pacientes_select.append(paciente_select)
    return pacientes_select
