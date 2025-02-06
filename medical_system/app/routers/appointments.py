from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Appointment, Doctor, Patient
from ..schemas import AppointmentCreate
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Rota para página de adicionar agendamento
@router.get("/dashboard/appointments/add", response_class=HTMLResponse)
async def add_appointment_page(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    doctors = db.query(Doctor).filter(Doctor.user_id == current_user.id).all()
    patients = db.query(Patient).filter(Patient.user_id == current_user.id).all()
    return templates.TemplateResponse("dashboard/add_appointment.html", {
        "request": request,
        "doctors": doctors,
        "patients": patients
    })

# Rota para adicionar agendamento
@router.post("/dashboard/appointments/add")
async def add_appointment(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    form_data = await request.form()
    appointment = Appointment(
        date=datetime.strptime(form_data.get("date"), "%Y-%m-%dT%H:%M"),
        doctor_id=form_data.get("doctor_id"),
        patient_id=form_data.get("patient_id"),
        user_id=current_user.id
    )
    db.add(appointment)
    db.commit()
    return RedirectResponse(url="/dashboard/appointments", status_code=303)

# Rota para página de editar agendamento
@router.get("/dashboard/appointments/edit/{appointment_id}", response_class=HTMLResponse)
async def edit_appointment_page(request: Request, appointment_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id, Appointment.user_id == current_user.id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    doctors = db.query(Doctor).filter(Doctor.user_id == current_user.id).all()
    patients = db.query(Patient).filter(Patient.user_id == current_user.id).all()
    return templates.TemplateResponse("dashboard/edit_appointment.html", {
        "request": request,
        "appointment": appointment,
        "doctors": doctors,
        "patients": patients
    })

# Rota para editar agendamento
@router.post("/dashboard/appointments/edit/{appointment_id}")
async def edit_appointment(request: Request, appointment_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    form_data = await request.form()
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id, Appointment.user_id == current_user.id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    appointment.date = datetime.strptime(form_data.get("date"), "%Y-%m-%dT%H:%M")
    appointment.doctor_id = form_data.get("doctor_id")
    appointment.patient_id = form_data.get("patient_id")
    db.commit()
    return RedirectResponse(url="/dashboard/appointments", status_code=303)

# Rota para deletar agendamento
@router.get("/dashboard/appointments/delete/{appointment_id}")
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id, Appointment.user_id == current_user.id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    db.delete(appointment)
    db.commit()
    return RedirectResponse(url="/dashboard/appointments", status_code=303)
