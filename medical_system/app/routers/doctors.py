from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Doctor
from ..schemas import DoctorCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard/doctors/add", response_class=HTMLResponse)
async def add_doctor_page(request: Request):
    return templates.TemplateResponse("dashboard/add_doctor.html", {"request": request})

@router.post("/dashboard/doctors/add")
async def add_doctor(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    form_data = await request.form()
    doctor = Doctor(
        name=form_data.get("name"),
        specialty=form_data.get("specialty"),
        phone=form_data.get("phone"),
        user_id=current_user.id
    )
    db.add(doctor)
    db.commit()
    return RedirectResponse(url="/dashboard/doctors", status_code=303)

@router.get("/dashboard/doctors/edit/{doctor_id}", response_class=HTMLResponse)
async def edit_doctor_page(request: Request, doctor_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id, Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return templates.TemplateResponse("dashboard/edit_doctor.html", {
        "request": request,
        "doctor": doctor
    })

@router.post("/dashboard/doctors/edit/{doctor_id}")
async def edit_doctor(request: Request, doctor_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    form_data = await request.form()
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id, Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    doctor.name = form_data.get("name")
    doctor.specialty = form_data.get("specialty")
    doctor.phone = form_data.get("phone")
    db.commit()
    return RedirectResponse(url="/dashboard/doctors", status_code=303)

@router.get("/dashboard/doctors/delete/{doctor_id}")
async def delete_doctor(doctor_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id, Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    db.delete(doctor)
    db.commit()
    return RedirectResponse(url="/dashboard/doctors", status_code=303)