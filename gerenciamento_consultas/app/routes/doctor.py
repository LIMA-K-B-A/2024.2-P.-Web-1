from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.schemas import DoctorCreate, Doctor
from app.models import Doctor as DoctorModel
from app.database import SessionLocal

router = APIRouter()

# Configuração do Jinja2 para templates
templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[Doctor])
def get_doctors():
    db = SessionLocal()
    doctors = db.query(DoctorModel).all()
    db.close()
    return doctors

@router.post("/doctors/add", response_model=Doctor)
def create_doctor(doctor: DoctorCreate):
    db = SessionLocal()
    db_doctor = DoctorModel(name=doctor.name, specialty=doctor.specialty, years_of_experience=doctor.years_of_experience)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    db.close()
    return db_doctor

@router.put("/{id}", response_model=Doctor)
def update_doctor(id: int, doctor: DoctorCreate):
    db = SessionLocal()
    db_doctor = db.query(DoctorModel).filter(DoctorModel.id == id).first()
    if not db_doctor:
        db.close()
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    db_doctor.name = doctor.name
    db_doctor.specialty = doctor.specialty
    db_doctor.years_of_experience = doctor.years_of_experience
    db.commit()
    db.refresh(db_doctor)
    db.close()
    return db_doctor

@router.delete("/{id}")
def delete_doctor(id: int):
    db = SessionLocal()
    db_doctor = db.query(DoctorModel).filter(DoctorModel.id == id).first()
    if not db_doctor:
        db.close()
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    db.delete(db_doctor)
    db.commit()
    db.close()
    return {"message": "Médico deletado com sucesso"}