from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.schemas import PatientCreate, Patient
from app.models import Patient as PatientModel
from app.database import SessionLocal

router = APIRouter()

@router.get("/", response_model=list[Patient])
def get_patients():
    db = SessionLocal()
    patients = db.query(PatientModel).all()
    db.close()
    return patients

@router.post("/", response_model=Patient)
def create_patient(patient: PatientCreate):
    db = SessionLocal()
    db_patient = PatientModel(name=patient.name, age=patient.age, condition=patient.condition)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    db.close()
    return db_patient

@router.put("/{id}", response_model=Patient)
def update_patient(id: int, patient: PatientCreate):
    db = SessionLocal()
    db_patient = db.query(PatientModel).filter(PatientModel.id == id).first()
    if not db_patient:
        db.close()
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    db_patient.name = patient.name
    db_patient.age = patient.age
    db_patient.condition = patient.condition
    db.commit()
    db.refresh(db_patient)
    db.close()
    return db_patient

@router.delete("/{id}")
def delete_patient(id: int):
    db = SessionLocal()
    db_patient = db.query(PatientModel).filter(PatientModel.id == id).first()
    if not db_patient:
        db.close()
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    db.delete(db_patient)
    db.commit()
    db.close()
    return {"message": "Paciente deletado com sucesso"}