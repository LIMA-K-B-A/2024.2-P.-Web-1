from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Patient, User
from ..schemas import PatientCreate, PatientUpdate
from ..routes.auth import get_current_user
from fastapi.templating import Jinja2Templates
from pathlib import Path

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

router = APIRouter()

@router.get("/patients", response_class=HTMLResponse)
async def list_patients(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "doctor"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    patients = db.query(Patient).all()
    return templates.TemplateResponse(
        "dashboard/patient.html",
        {"request": request, "patients": patients}
    )

@router.get("/patients/{patient_id}", response_class=HTMLResponse)
async def get_patient(
    patient_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    return templates.TemplateResponse("dashboard/view_patient.html", {
        "request": request,
        "patient": patient
    })

@router.post("/patients", response_class=RedirectResponse)
async def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    return RedirectResponse(url="/patients", status_code=303)

@router.put("/patients/{patient_id}", response_class=RedirectResponse)
async def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    for key, value in patient.dict().items():
        setattr(db_patient, key, value)
    
    db.commit()
    db.refresh(db_patient)
    return RedirectResponse(url="/patients", status_code=303)

@router.delete("/patients/{patient_id}", response_class=RedirectResponse)
async def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    db.delete(db_patient)
    db.commit()
    return RedirectResponse(url="/patients", status_code=303)
