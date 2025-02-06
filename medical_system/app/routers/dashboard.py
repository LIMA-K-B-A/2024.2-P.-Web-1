from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Doctor, Patient, Appointment

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    doctors = db.query(Doctor).filter(Doctor.user_id == current_user.id).all()
    patients = db.query(Patient).filter(Patient.user_id == current_user.id).all()
    appointments = db.query(Appointment).filter(Appointment.user_id == current_user.id).all()
    return templates.TemplateResponse("dashboard/index.html", {
        "request": request,
        "doctors": doctors,
        "patients": patients,
        "appointments": appointments
    })

@router.get("/dashboard/doctors", response_class=HTMLResponse)
async def doctors_list(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    doctors = db.query(Doctor).filter(Doctor.user_id == current_user.id).all()
    return templates.TemplateResponse("dashboard/doctors.html", {
        "request": request,
        "doctors": doctors
    })

@router.get("/dashboard/patients", response_class=HTMLResponse)
async def patients_list(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    patients = db.query(Patient).filter(Patient.user_id == current_user.id).all()
    return templates.TemplateResponse("dashboard/patients.html", {
        "request": request,
        "patients": patients
    })

@router.get("/dashboard/appointments", response_class=HTMLResponse)
async def appointments_list(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    appointments = db.query(Appointment).filter(Appointment.user_id == current_user.id).all()
    return templates.TemplateResponse("dashboard/appointments.html", {
        "request": request,
        "appointments": appointments
    })