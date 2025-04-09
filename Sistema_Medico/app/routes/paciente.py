from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Paciente, Usuario, TipoUsuario
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional
from app.core.security import get_password_hash

router = APIRouter()

class PacienteCreate(BaseModel):
    nome: str
    email: str
    cpf: str
    data_nascimento: str
    telefone: str
    endereco: Optional[str] = None

class PacienteList(BaseModel):
    id: int
    nome: str
    email: str
    cpf: str
    data_nascimento: date
    telefone: str
    endereco: Optional[str] = None

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
            data_nascimento=paciente.data_nascimento.date(),
            telefone=paciente.telefone,
            endereco=paciente.endereco
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

        # Converte a string de data para objeto datetime
        try:
            data_nascimento = datetime.strptime(paciente.data_nascimento, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD")

        # Cria o usuário primeiro com uma senha padrão
        senha_padrao = "paciente123"  # Senha padrão para pacientes
        usuario = Usuario(
            nome=paciente.nome,
            email=paciente.email,
            senha=get_password_hash(senha_padrao),
            tipo_usuario=TipoUsuario.PACIENTE
        )
        db.add(usuario)
        db.flush()  # Garante que o ID do usuário seja gerado

        # Cria o paciente vinculado ao usuário
        paciente_db = Paciente(
            usuario_id=usuario.id,
            cpf=paciente.cpf,
            data_nascimento=data_nascimento,
            telefone=paciente.telefone,
            endereco=paciente.endereco or ""
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
            "telefone": paciente_db.telefone,
            "endereco": paciente_db.endereco
        }
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

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
        "telefone": paciente.telefone,
        "endereco": paciente.endereco if hasattr(paciente, 'endereco') else ""
    }

@router.put("/{paciente_id}")
async def atualizar_paciente(
    paciente_id: int,
    paciente_data: dict,
    db: Session = Depends(get_db)
):
    """Atualiza um paciente."""
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    # Atualiza os dados do paciente
    if "cpf" in paciente_data:
        paciente.cpf = paciente_data["cpf"]
    if "data_nascimento" in paciente_data:
        paciente.data_nascimento = paciente_data["data_nascimento"]
    if "telefone" in paciente_data:
        paciente.telefone = paciente_data["telefone"]
    if "endereco" in paciente_data:
        paciente.endereco = paciente_data["endereco"]
    
    # Atualiza os dados do usuário
    usuario = db.query(Usuario).filter(Usuario.id == paciente.usuario_id).first()
    if usuario:
        if "nome" in paciente_data:
            usuario.nome = paciente_data["nome"]
        if "email" in paciente_data:
            # Verifica se o novo email já está em uso por outro usuário
            email_existente = db.query(Usuario).filter(
                Usuario.email == paciente_data["email"], 
                Usuario.id != paciente.usuario_id
            ).first()
            if email_existente:
                raise HTTPException(status_code=400, detail="Email já está em uso")
            usuario.email = paciente_data["email"]
    
    db.commit()
    db.refresh(paciente)
    
    return {
        "id": paciente.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "cpf": paciente.cpf,
        "data_nascimento": paciente.data_nascimento,
        "telefone": paciente.telefone,
        "endereco": paciente.endereco if hasattr(paciente, 'endereco') else ""
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

@router.get("/select")
async def listar_pacientes_select(db: Session = Depends(get_db)):
    """Lista pacientes em formato simplificado para select."""
    try:
        # Busca usuários que são pacientes e faz join com a tabela de pacientes
        pacientes = db.query(Usuario, Paciente).join(
            Paciente, Usuario.id == Paciente.usuario_id
        ).filter(
            Usuario.tipo_usuario == TipoUsuario.PACIENTE
        ).all()
        
        pacientes_select = []
        for usuario, paciente in pacientes:
            pacientes_select.append({
                "id": paciente.id,
                "nome": usuario.nome,
                "cpf": paciente.cpf
            })
        return pacientes_select
    except Exception as e:
        print(f"Erro ao buscar pacientes: {str(e)}")  # Log do erro
        raise HTTPException(status_code=500, detail=str(e))
