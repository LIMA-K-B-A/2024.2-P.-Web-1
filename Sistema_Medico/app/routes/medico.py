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
    medico = db.query(Medico).join(Usuario).filter(Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    return {
        "id": medico.id,
        "nome": medico.usuario.nome,
        "email": medico.usuario.email,
        "crm": medico.crm,
        "especialidade": medico.especialidade,
        "horario_atendimento": medico.horario_atendimento
    }

@router.put("/{medico_id}")
async def atualizar_medico(
    medico_id: int,
    medico_data: dict,
    db: Session = Depends(get_db)
):
    """Atualiza um médico."""
    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    # Atualiza os dados do médico
    if "crm" in medico_data:
        # Verifica se o CRM já está em uso por outro médico
        crm_existente = db.query(Medico).filter(
            Medico.crm == medico_data["crm"], 
            Medico.id != medico_id
        ).first()
        if crm_existente:
            raise HTTPException(status_code=400, detail="CRM já está em uso")
        medico.crm = medico_data["crm"]
        
    if "especialidade" in medico_data:
        medico.especialidade = medico_data["especialidade"]
        
    if "horario_atendimento" in medico_data:
        medico.horario_atendimento = medico_data["horario_atendimento"]
    
    # Atualiza os dados do usuário
    usuario = db.query(Usuario).filter(Usuario.id == medico.usuario_id).first()
    if usuario:
        if "nome" in medico_data:
            usuario.nome = medico_data["nome"]
            
        if "email" in medico_data:
            # Verifica se o email já está em uso por outro usuário
            email_existente = db.query(Usuario).filter(
                Usuario.email == medico_data["email"], 
                Usuario.id != medico.usuario_id
            ).first()
            if email_existente:
                raise HTTPException(status_code=400, detail="Email já está em uso")
            usuario.email = medico_data["email"]
            
        # Atualiza a senha apenas se fornecida
        if "senha" in medico_data and medico_data["senha"]:
            usuario.senha = medico_data["senha"]

    db.commit()
    db.refresh(medico)
    db.refresh(usuario)
    
    return {
        "id": medico.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "crm": medico.crm,
        "especialidade": medico.especialidade,
        "horario_atendimento": medico.horario_atendimento
    }

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

@router.get("/select")
async def listar_medicos_select(db: Session = Depends(get_db)):
    """Lista médicos em formato simplificado para select."""
    try:
        # Busca usuários que são médicos e faz join com a tabela de médicos
        medicos = db.query(Usuario, Medico).join(
            Medico, Usuario.id == Medico.usuario_id
        ).filter(
            Usuario.tipo_usuario == TipoUsuario.MEDICO
        ).all()
        
        medicos_select = []
        for usuario, medico in medicos:
            medicos_select.append({
                "id": medico.id,
                "nome": usuario.nome,
                "especialidade": medico.especialidade
            })
        return medicos_select
    except Exception as e:
        print(f"Erro ao buscar médicos: {str(e)}")  # Log do erro
        raise HTTPException(status_code=500, detail=str(e))
