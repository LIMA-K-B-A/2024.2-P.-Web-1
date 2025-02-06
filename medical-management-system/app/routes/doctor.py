from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Doctor, User
from ..schemas import DoctorCreate, DoctorUpdate
from ..routes.auth import get_current_user
from fastapi.templating import Jinja2Templates
from pathlib import Path

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

router = APIRouter()

@router.get("/doctors", response_class=HTMLResponse)
async def list_doctors(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    doctors = db.query(Doctor).all()
    return templates.TemplateResponse("dashboard/doctor.html", {
        "request": request,
        "doctors": doctors
    })

@router.get("/doctors/{doctor_id}", response_class=HTMLResponse)
async def get_doctor(
    doctor_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    return templates.TemplateResponse("dashboard/view_doctor.html", {
        "request": request,
        "doctor": doctor
    })

@router.post("/doctors", response_class=RedirectResponse)
async def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    return RedirectResponse(url="/doctors", status_code=303)

@router.put("/doctors/{doctor_id}", response_class=RedirectResponse)
async def update_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    for key, value in doctor.dict().items():
        setattr(db_doctor, key, value)
    
    db.commit()
    db.refresh(db_doctor)
    return RedirectResponse(url="/doctors", status_code=303)

@router.delete("/doctors/{doctor_id}", response_class=RedirectResponse)
async def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    db.delete(db_doctor)
    db.commit()
    return RedirectResponse(url="/doctors", status_code=303)
