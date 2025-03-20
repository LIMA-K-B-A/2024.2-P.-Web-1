from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Appointment, Patient, Doctor
from ..schemas import AppointmentCreate, AppointmentUpdate
from fastapi.templating import Jinja2Templates
from datetime import datetime
from pathlib import Path

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

router = APIRouter()

# Rota para listar todas as consultas
@router.get("/appointments", response_class=HTMLResponse)
async def list_appointments(request: Request, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    return templates.TemplateResponse("dashboard/appointments.html", {"request": request, "appointments": appointments})

# Rota para adicionar uma nova consulta
@router.get("/appointments/add", response_class=HTMLResponse)
async def add_appointment(request: Request, db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    patients = db.query(Patient).all()
    return templates.TemplateResponse("dashboard/add_appointment.html", {"request": request, "doctors": doctors, "patients": patients})

# Rota para criar uma nova consulta (POST)
@router.post("/appointments/create", response_class=HTMLResponse)
async def create_appointment(request: Request, appointment: AppointmentCreate, db: Session = Depends(get_db)):
    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_time=appointment.appointment_time,
        status=appointment.status
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return templates.TemplateResponse("dashboard/appointments.html", {"request": request, "appointments": db.query(Appointment).all()})

# Rota para editar uma consulta
@router.get("/appointments/edit/{appointment_id}", response_class=HTMLResponse)
async def edit_appointment(appointment_id: int, request: Request, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    doctors = db.query(Doctor).all()
    patients = db.query(Patient).all()
    return templates.TemplateResponse("dashboard/edit_appointment.html", {"request": request, "appointment": appointment, "doctors": doctors, "patients": patients})

# Rota para atualizar uma consulta (PUT)
@router.put("/appointments/update/{appointment_id}", response_class=HTMLResponse)
async def update_appointment(appointment_id: int, request: Request, appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    appointment_to_update = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment_to_update:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment_to_update.patient_id = appointment.patient_id
    appointment_to_update.doctor_id = appointment.doctor_id
    appointment_to_update.appointment_time = appointment.appointment_time
    appointment_to_update.status = appointment.status
    db.commit()
    db.refresh(appointment_to_update)
    return templates.TemplateResponse("dashboard/appointments.html", {"request": request, "appointments": db.query(Appointment).all()})

# Rota para excluir uma consulta (DELETE)
@router.delete("/appointments/delete/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    db.delete(appointment)
    db.commit()
    return {"detail": "Appointment deleted successfully"}
