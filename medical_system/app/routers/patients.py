from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Patient
from ..schemas import PatientCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard/patients/add", response_class=HTMLResponse)
async def add_patient_page(request: Request):
    return templates.TemplateResponse("dashboard/add_patient.html", {"request": request})

@router.post("/dashboard/patients/add")
async def add_patient(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    form_data = await request.form()
    patient = Patient(
        name=form_data.get("name"),
        age=form_data.get("age"),
        phone=form_data.get("phone"),
        user_id=current_user.id
    )
    db.add(patient)
    db.commit()
    return RedirectResponse(url="/dashboard/patients", status_code=303)

@router.get("/dashboard/patients/edit/{patient_id}", response_class=HTMLResponse)
async def edit_patient_page(request: Request, patient_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return templates.TemplateResponse("dashboard/edit_patient.html", {
        "request": request,
        "patient": patient
    })

@router.post("/dashboard/patients/edit/{patient_id}")
async def edit_patient(request: Request, patient_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    form_data = await request.form()
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    patient.name = form_data.get("name")
    patient.age = form_data.get("age")
    patient.phone = form_data.get("phone")
    db.commit()
    return RedirectResponse(url="/dashboard/patients", status_code=303)

@router.get("/dashboard/patients/delete/{patient_id}")
async def delete_patient(patient_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    db.delete(patient)
    db.commit()
    return RedirectResponse(url="/dashboard/patients", status_code=303)