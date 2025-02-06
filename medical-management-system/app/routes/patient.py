# app/routes/patient.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas  # Corrigir importações para usar os modelos corretos
from datetime import datetime
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/appointments", response_model=list[schemas.Appointment])
async def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(models.Appointment).all()
    return appointments

@router.get("/appointments/{appointment_id}", response_model=schemas.Appointment)
async def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.post("/appointments", response_model=schemas.Appointment)
async def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = models.Appointment(**appointment.dict())  # Certificando que estamos criando corretamente
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.put("/appointments/{appointment_id}", response_model=schemas.Appointment)
async def update_appointment(appointment_id: int, appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for key, value in appointment.dict().items():
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.delete("/appointments/{appointment_id}", response_model=schemas.Appointment)
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(db_appointment)
    db.commit()
    return db_appointment
