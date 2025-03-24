from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar uma consulta
@router.post("/", response_model=schemas.ConsultaOut)
async def create_consulta(consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    print(f"Recebido data: {consulta.data}, Tipo: {type(consulta.data)}")  # Log para depuração
    print(f"Recebido hora: {consulta.hora}, Tipo: {type(consulta.hora)}")  # Log para depuração

    try:
        data_obj = consulta.data  # Já é datetime.date
        hora_obj = consulta.hora  # Já é datetime.time
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar data ou hora: {str(e)}")
    
    db_consulta = models.Consulta(
        paciente_id=consulta.paciente_id,
        medico_id=consulta.medico_id,
        data=data_obj,
        hora=hora_obj,
        descricao=consulta.descricao
    )
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

# Rota para listar todas as consultas
@router.get("/", response_model=list[schemas.ConsultaOut])
def get_consultas(db: Session = Depends(get_db)):
    consultas = db.query(models.Consulta).all()
    return consultas

# Rota para obter uma consulta por ID
@router.get("/{consulta_id}", response_model=schemas.ConsultaOut)
def get_consulta(consulta_id: int, db: Session = Depends(get_db)):
    consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return consulta

# Rota para atualizar uma consulta
@router.put("/{consulta_id}", response_model=schemas.ConsultaOut)
def update_consulta(consulta_id: int, consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    db_consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not db_consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    try:
        # Atualizando os campos
        db_consulta.paciente_id = consulta.paciente_id
        db_consulta.medico_id = consulta.medico_id
        db_consulta.data = consulta.data  # Atualizando com 'data' recebida
        db_consulta.hora = consulta.hora  # Atualizando com 'hora' recebida
        db_consulta.descricao = consulta.descricao  # Atualizando com 'descricao'
        
        # Commit e refresh para garantir que a atualização seja salva
        db.commit()
        db.refresh(db_consulta)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar data ou hora: {str(e)}")
    
    return db_consulta

# Rota para deletar uma consulta
@router.delete("/{consulta_id}", response_model=schemas.ConsultaOut)
def delete_consulta(consulta_id: int, db: Session = Depends(get_db)):
    db_consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not db_consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    db.delete(db_consulta)
    db.commit()
    return db_consulta
