# router/pacientes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/pacientes", response_model=list[schemas.Paciente])
def read_pacientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_pacientes(db, skip, limit)

@router.get("/pacientes/{paciente_id}", response_model=schemas.Paciente)
def read_paciente(paciente_id: int, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente(db, paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return db_paciente

@router.post("/pacientes", response_model=schemas.Paciente)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.create_paciente(db=db, paciente=paciente)

@router.put("/pacientes/{paciente_id}", response_model=schemas.Paciente)
def update_paciente(paciente_id: int, paciente: schemas.PacienteUpdate, db: Session = Depends(get_db)):
    db_paciente = crud.update_paciente(db, paciente_id, paciente)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return db_paciente

@router.delete("/pacientes/{paciente_id}")
def delete_paciente(paciente_id: int, db: Session = Depends(get_db)):
    success = crud.delete_paciente(db, paciente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return {"message": "Paciente deletado com sucesso"}