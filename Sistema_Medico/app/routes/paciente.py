from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Paciente
from datetime import date

router = APIRouter()

@router.get("/")
async def listar_pacientes(db: Session = Depends(get_db)):
    """Lista todos os pacientes."""
    return db.query(Paciente).all()

@router.post("/")
async def criar_paciente(
    nome: str,
    cpf: str,
    email: str = None,
    telefone: str = None,
    data_nascimento: date = None,
    endereco: str = None,
    db: Session = Depends(get_db)
):
    """Cria um novo paciente."""
    # Verifica se o CPF já está em uso
    if db.query(Paciente).filter(Paciente.cpf == cpf).first():
        raise HTTPException(status_code=400, detail="CPF já está em uso")

    # Cria o paciente
    paciente = Paciente(
        nome=nome,
        cpf=cpf,
        email=email,
        telefone=telefone,
        data_nascimento=data_nascimento,
        endereco=endereco
    )

    db.add(paciente)
    db.commit()
    db.refresh(paciente)

    return paciente

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
    nome: str = None,
    email: str = None,
    telefone: str = None,
    data_nascimento: date = None,
    endereco: str = None,
    db: Session = Depends(get_db)
):
    """Atualiza um paciente."""
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    if nome:
        paciente.nome = nome
    if email:
        paciente.email = email
    if telefone:
        paciente.telefone = telefone
    if data_nascimento:
        paciente.data_nascimento = data_nascimento
    if endereco:
        paciente.endereco = endereco

    db.commit()
    db.refresh(paciente)
    return paciente

@router.delete("/{paciente_id}")
async def deletar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Deleta um paciente."""
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    db.delete(paciente)
    db.commit()
    return {"message": "Paciente deletado com sucesso"}
