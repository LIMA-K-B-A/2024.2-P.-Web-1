from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.models import Doctor as DoctorModel

router = APIRouter()

# Função para obter a sessão do banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/doctors/", response_model=schemas.Doctor)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.name == doctor.name).first()
    if db_doctor:
        raise HTTPException(status_code=400, detail="Doctor already registered")
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.get("/doctors/", response_model=list[schemas.Doctor])
def get_doctors(db: Session = Depends(get_db)):
    return db.query(models.Doctor).all()

@router.get("/doctors/{doctor_id}", response_model=schemas.Doctor)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor

@router.put("/doctors/{doctor_id}", response_model=schemas.Doctor)
def update_doctor(doctor_id: int, doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db_doctor.name = doctor.name
    db_doctor.specialty = doctor.specialty
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.delete("/doctors/{doctor_id}", status_code=204)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(db_doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}
