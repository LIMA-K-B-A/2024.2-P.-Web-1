# router/consultas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/consultas", response_model=list[schemas.Consulta])
def read_consultas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_consultas(db, skip, limit)

@router.get("/consultas/{consulta_id}", response_model=schemas.Consulta)
def read_consulta(consulta_id: int, db: Session = Depends(get_db)):
    db_consulta = crud.get_consulta(db, consulta_id)
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return db_consulta

@router.post("/consultas", response_model=schemas.Consulta)
def create_consulta(consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    return crud.create_consulta(db=db, consulta=consulta)

@router.put("/consultas/{consulta_id}", response_model=schemas.Consulta)
def update_consulta(consulta_id: int, consulta: schemas.ConsultaUpdate, db: Session = Depends(get_db)):
    db_consulta = crud.update_consulta(db, consulta_id, consulta)
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return db_consulta

@router.delete("/consultas/{consulta_id}")
def delete_consulta(consulta_id: int, db: Session = Depends(get_db)):
    success = crud.delete_consulta(db, consulta_id)
    if not success:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return {"message": "Consulta deletada com sucesso"}