from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Usuario, TipoUsuario, Medico, Paciente
from typing import List

router = APIRouter()

@router.get("/medicos")
async def listar_usuarios_medicos(db: Session = Depends(get_db)):
    """Lista usuários que são médicos."""
    try:
        medicos = db.query(Usuario, Medico).join(
            Medico, Usuario.id == Medico.usuario_id
        ).filter(
            Usuario.tipo_usuario == TipoUsuario.MEDICO
        ).all()
        
        return [
            {
                "id": medico.id,
                "nome": usuario.nome,
                "especialidade": medico.especialidade
            }
            for usuario, medico in medicos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pacientes")
async def listar_usuarios_pacientes(db: Session = Depends(get_db)):
    """Lista usuários que são pacientes."""
    try:
        pacientes = db.query(Usuario, Paciente).join(
            Paciente, Usuario.id == Paciente.usuario_id
        ).filter(
            Usuario.tipo_usuario == TipoUsuario.PACIENTE
        ).all()
        
        return [
            {
                "id": paciente.id,
                "nome": usuario.nome,
                "cpf": paciente.cpf
            }
            for usuario, paciente in pacientes
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 