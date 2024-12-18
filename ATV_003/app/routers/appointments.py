from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas

router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criar uma consulta
@router.post("/", response_model=schemas.AppointmentResponse)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# Buscar uma consulta por ID
@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return appointment

# Buscar todas as consultas
@router.get("/", response_model=list[schemas.AppointmentResponse])
def read_appointments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    appointments = db.query(models.Appointment).offset(skip).limit(limit).all()
    return appointments

# Atualizar uma consulta
@router.put("/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment(appointment_id: int, updated_appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    for key, value in updated_appointment.dict().items():
        setattr(appointment, key, value)
    db.commit()
    db.refresh(appointment)
    return appointment

# Deletar uma consulta
@router.delete("/{appointment_id}", response_model=schemas.AppointmentResponse)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    db.delete(appointment)
    db.commit()
    return appointment
