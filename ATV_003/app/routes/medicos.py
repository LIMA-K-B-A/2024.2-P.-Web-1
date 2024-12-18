# router/medicos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/medicos", response_model=list[schemas.Medico])
def read_medicos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_medicos(db, skip, limit)

@router.get("/medicos/{medico_id}", response_model=schemas.Medico)
def read_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = crud.get_medico(db, medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return db_medico

@router.post("/medicos", response_model=schemas.Medico)
def create_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    return crud.create_medico(db=db, medico=medico)

@router.put("/medicos/{medico_id}", response_model=schemas.Medico)
def update_medico(medico_id: int, medico: schemas.MedicoUpdate, db: Session = Depends(get_db)):
    db_medico = crud.update_medico(db, medico_id, medico)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return db_medico

@router.delete("/medicos/{medico_id}")
def delete_medico(medico_id: int, db: Session = Depends(get_db)):
    success = crud.delete_medico(db, medico_id)
    if not success:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return {"message": "Médico deletado com sucesso"}
