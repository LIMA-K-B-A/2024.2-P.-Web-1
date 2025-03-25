from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Consulta, Medico, Paciente
from app.models import StatusConsulta
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

router = APIRouter()

class ConsultaCreate(BaseModel):
    paciente_id: int
    medico_id: int
    data_hora: datetime
    tipo_consulta: str
    status: str = StatusConsulta.AGENDADA
    observacoes: Optional[str] = None

class ConsultaList(BaseModel):
    id: int
    paciente_id: int
    medico_id: int
    data_hora: datetime
    tipo_consulta: str
    status: str
    observacoes: Optional[str] = None
    paciente: dict
    medico: dict

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ConsultaList])
async def listar_consultas(db: Session = Depends(get_db)):
    """Lista todas as consultas."""
    consultas = db.query(Consulta).all()
    consultas_list = []
    for consulta in consultas:
        consulta_dict = ConsultaList(
            id=consulta.id,
            paciente_id=consulta.paciente_id,
            medico_id=consulta.medico_id,
            data_hora=consulta.data_hora,
            tipo_consulta=consulta.tipo_consulta,
            status=consulta.status,
            observacoes=consulta.observacoes,
            paciente={
                "id": consulta.paciente.id,
                "nome": consulta.paciente.usuario.nome,
                "cpf": consulta.paciente.cpf
            },
            medico={
                "id": consulta.medico.id,
                "nome": consulta.medico.usuario.nome,
                "especialidade": consulta.medico.especialidade
            }
        )
        consultas_list.append(consulta_dict)
    return consultas_list

@router.post("/")
async def criar_consulta(
    consulta: ConsultaCreate,
    db: Session = Depends(get_db)
):
    """Cria uma nova consulta."""
    try:
        # Verifica se o paciente existe
        paciente = db.query(Paciente).filter(Paciente.id == consulta.paciente_id).first()
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")

        # Verifica se o médico existe
        medico = db.query(Medico).filter(Medico.id == consulta.medico_id).first()
        if not medico:
            raise HTTPException(status_code=404, detail="Médico não encontrado")

        # Cria a consulta
        consulta_db = Consulta(
            paciente_id=consulta.paciente_id,
            medico_id=consulta.medico_id,
            data_hora=consulta.data_hora,
            tipo_consulta=consulta.tipo_consulta,
            status=consulta.status,
            observacoes=consulta.observacoes
        )

        db.add(consulta_db)
        db.commit()
        db.refresh(consulta_db)

        return {
            "id": consulta_db.id,
            "paciente_id": consulta_db.paciente_id,
            "medico_id": consulta_db.medico_id,
            "data_hora": consulta_db.data_hora,
            "tipo_consulta": consulta_db.tipo_consulta,
            "status": consulta_db.status,
            "observacoes": consulta_db.observacoes,
            "paciente": {
                "id": paciente.id,
                "nome": paciente.usuario.nome,
                "cpf": paciente.cpf
            },
            "medico": {
                "id": medico.id,
                "nome": medico.usuario.nome,
                "especialidade": medico.especialidade
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{consulta_id}")
async def obter_consulta(consulta_id: int, db: Session = Depends(get_db)):
    """Obtém uma consulta pelo ID."""
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    return {
        "id": consulta.id,
        "paciente_id": consulta.paciente_id,
        "medico_id": consulta.medico_id,
        "data_hora": consulta.data_hora,
        "tipo_consulta": consulta.tipo_consulta,
        "status": consulta.status,
        "observacoes": consulta.observacoes,
        "paciente": {
            "id": consulta.paciente.id,
            "nome": consulta.paciente.usuario.nome,
            "cpf": consulta.paciente.cpf
        },
        "medico": {
            "id": consulta.medico.id,
            "nome": consulta.medico.usuario.nome,
            "especialidade": consulta.medico.especialidade
        }
    }

@router.put("/{consulta_id}")
async def atualizar_consulta(
    consulta_id: int,
    consulta: ConsultaCreate,
    db: Session = Depends(get_db)
):
    """Atualiza uma consulta."""
    consulta_db = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta_db:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    # Verifica se o paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == consulta.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Verifica se o médico existe
    medico = db.query(Medico).filter(Medico.id == consulta.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    # Atualiza os campos
    consulta_db.paciente_id = consulta.paciente_id
    consulta_db.medico_id = consulta.medico_id
    consulta_db.data_hora = consulta.data_hora
    consulta_db.tipo_consulta = consulta.tipo_consulta
    consulta_db.status = consulta.status
    consulta_db.observacoes = consulta.observacoes

    db.commit()
    db.refresh(consulta_db)
    return consulta_db

@router.delete("/{consulta_id}")
async def deletar_consulta(consulta_id: int, db: Session = Depends(get_db)):
    """Deleta uma consulta."""
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    db.delete(consulta)
    db.commit()
    return {"message": "Consulta deletada com sucesso"}
