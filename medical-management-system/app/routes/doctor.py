from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Doctor, User
from ..schemas import DoctorCreate
from ..routes.auth import get_current_user

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
    return templates.TemplateResponse(
        "doctors.html",
        {"request": request, "doctors": doctors}
    )