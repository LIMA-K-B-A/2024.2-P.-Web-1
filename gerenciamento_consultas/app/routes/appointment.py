from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

# Função para obter a sessão do banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/appointments/", response_model=schemas.Appointment)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.get("/appointments/", response_model=list[schemas.Appointment])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).all()

@router.get("/appointments/{appointment_id}", response_model=schemas.Appointment)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@router.put("/appointments/{appointment_id}", response_model=schemas.Appointment)
def update_appointment(appointment_id: int, appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db_appointment.date = appointment.date
    db_appointment.patient_id = appointment.patient_id
    db_appointment.doctor_id = appointment.doctor_id
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.delete("/appointments/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(db_appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}
