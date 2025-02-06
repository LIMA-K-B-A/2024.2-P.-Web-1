from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Doctor
from ..schemas import DoctorCreate, Doctor
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

# GET: Lista todos os médicos
@router.get("/doctors", response_model=list[Doctor])
async def get_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    return doctors

# GET: Obtém um médico pelo ID
@router.get("/doctors/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

# POST: Cria um novo médico
@router.post("/doctors", response_model=Doctor)
async def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

# PUT: Atualiza um médico existente
@router.put("/doctors/{doctor_id}", response_model=Doctor)
async def update_doctor(doctor_id: int, doctor: DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    for key, value in doctor.dict().items():
        setattr(db_doctor, key, value)
    
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

# DELETE: Exclui um médico
@router.delete("/doctors/{doctor_id}", response_model=Doctor)
async def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.delete(db_doctor)
    db.commit()
    return db_doctor
