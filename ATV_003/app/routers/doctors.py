from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas

router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criar um médico
@router.post("/", response_model=schemas.DoctorResponse)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

# Buscar um médico por ID
@router.get("/{doctor_id}", response_model=schemas.DoctorResponse)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return doctor

# Buscar todos os médicos
@router.get("/", response_model=list[schemas.DoctorResponse])
def read_doctors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    doctors = db.query(models.Doctor).offset(skip).limit(limit).all()
    return doctors

# Atualizar um médico
@router.put("/{doctor_id}", response_model=schemas.DoctorResponse)
def update_doctor(doctor_id: int, updated_doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    for key, value in updated_doctor.dict().items():
        setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor

# Deletar um médico
@router.delete("/{doctor_id}", response_model=schemas.DoctorResponse)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    db.delete(doctor)
    db.commit()
    return doctor
