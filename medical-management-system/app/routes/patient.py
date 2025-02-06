from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Patient, User
from ..schemas import PatientCreate
from ..routes.auth import get_current_user

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
        "patients.html",
        {"request": request, "patients": patients}
    )

@router.post("/patients")
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