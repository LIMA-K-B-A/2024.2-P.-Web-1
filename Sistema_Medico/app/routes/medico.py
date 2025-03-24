from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Medico, Usuario, TipoUsuario
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/")
async def listar_medicos(db: Session = Depends(get_db)):
    """Lista todos os médicos."""
    return db.query(Medico).all()

@router.post("/")
async def criar_medico(
    nome: str,
    email: str,
    senha: str,
    crm: str,
    especialidade: str,
    horario_atendimento: str,
    db: Session = Depends(get_db)
):
    """Cria um novo médico."""
    # Verifica se o email já está em uso
    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status_code=400, detail="Email já está em uso")

    # Verifica se o CRM já está em uso
    if db.query(Medico).filter(Medico.crm == crm).first():
        raise HTTPException(status_code=400, detail="CRM já está em uso")

    # Cria o usuário
    usuario = Usuario(
        nome=nome,
        email=email,
        senha=get_password_hash(senha),
        tipo_usuario=TipoUsuario.MEDICO
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Cria o médico
    medico = Medico(
        usuario_id=usuario.id,
        crm=crm,
        especialidade=especialidade,
        horario_atendimento=horario_atendimento
    )

    db.add(medico)
    db.commit()
    db.refresh(medico)

    return medico

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
