from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Appointment, Patient, Doctor
from ..schemas import AppointmentCreate, Appointment
from ..schemas import AppointmentList
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

# GET: Lista todas as consultas
@router.get("/appointments", response_model=AppointmentList)
async def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    return AppointmentList(appointments=appointments)

# GET: Obtém uma consulta pelo ID
@router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

# POST: Cria uma nova consulta
@router.post("/appointments", response_model=Appointment)
async def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# PUT: Atualiza uma consulta existente
@router.put("/appointments/{appointment_id}", response_model=Appointment)
async def update_appointment(appointment_id: int, appointment: AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    for key, value in appointment.dict().items():
        setattr(db_appointment, key, value)
    
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# DELETE: Exclui uma consulta
@router.delete("/appointments/{appointment_id}", response_model=Appointment)
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    db.delete(db_appointment)
    db.commit()
    return db_appointment
