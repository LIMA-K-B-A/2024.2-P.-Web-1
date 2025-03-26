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
    consulta_data: dict,
    db: Session = Depends(get_db)
):
    """Atualiza uma consulta."""
    consulta_db = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta_db:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    # Verifica se o paciente existe, se foi fornecido
    if "paciente_id" in consulta_data:
        paciente = db.query(Paciente).filter(Paciente.id == consulta_data["paciente_id"]).first()
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        consulta_db.paciente_id = consulta_data["paciente_id"]

    # Verifica se o médico existe, se foi fornecido
    if "medico_id" in consulta_data:
        medico = db.query(Medico).filter(Medico.id == consulta_data["medico_id"]).first()
        if not medico:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        consulta_db.medico_id = consulta_data["medico_id"]

    # Atualiza outros campos
    if "data_hora" in consulta_data:
        consulta_db.data_hora = consulta_data["data_hora"]
    
    if "motivo" in consulta_data:
        consulta_db.tipo_consulta = consulta_data["motivo"]
    elif "tipo_consulta" in consulta_data:
        consulta_db.tipo_consulta = consulta_data["tipo_consulta"]
        
    if "status" in consulta_data:
        consulta_db.status = consulta_data["status"]
        
    if "observacoes" in consulta_data:
        consulta_db.observacoes = consulta_data["observacoes"]

    try:
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
                "id": consulta_db.paciente.id,
                "nome": consulta_db.paciente.usuario.nome,
                "cpf": consulta_db.paciente.cpf
            },
            "medico": {
                "id": consulta_db.medico.id,
                "nome": consulta_db.medico.usuario.nome,
                "especialidade": consulta_db.medico.especialidade
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{consulta_id}")
async def deletar_consulta(consulta_id: int, db: Session = Depends(get_db)):
    """Deleta uma consulta."""
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    db.delete(consulta)
    db.commit()
    return {"message": "Consulta deletada com sucesso"}
