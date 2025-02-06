from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Appointment, User
from ..schemas import AppointmentCreate
from ..routes.auth import get_current_user

router = APIRouter()

@router.get("/appointments", response_class=HTMLResponse)
async def list_appointments(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "patient":
        appointments = db.query(Appointment).filter(Appointment.patient_id == current_user.id).all()
    elif current_user.role == "doctor":
        appointments = db.query(Appointment).filter(Appointment.doctor_id == current_user.id).all()
    else:
        appointments = db.query(Appointment).all()
    
    return templates.TemplateResponse(
        "appointments.html",
        {"request": request, "appointments": appointments}
    )