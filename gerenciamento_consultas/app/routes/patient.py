# app/routes/patient.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.schemas import PatientCreate, Patient
from app.models import Patient as PatientModel  # Importação direta do modelo
from app.database import SessionLocal

router = APIRouter()

# Configuração do Jinja2 para templates
templates = Jinja2Templates(directory="templates")

# Função para gerenciar sessões do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def get_patients(request: Request, db: Session = Depends(get_db)):
    patients = db.query(PatientModel).all()
    return templates.TemplateResponse("patients.html", {"request": request, "patients": patients})

@router.post("/patients/add", response_model=Patient)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = PatientModel(name=patient.name, age=patient.age, condition=patient.condition)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.put("/{id}", response_model=Patient)
def update_patient(id: int, patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = db.query(PatientModel).filter(PatientModel.id == id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    db_patient.name = patient.name
    db_patient.age = patient.age
    db_patient.condition = patient.condition
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.delete("/{id}")
def delete_patient(id: int, db: Session = Depends(get_db)):
    db_patient = db.query(PatientModel).filter(PatientModel.id == id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    db.delete(db_patient)
    db.commit()
    return {"message": "Paciente deletado com sucesso"}