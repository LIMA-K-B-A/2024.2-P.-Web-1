from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.schemas import AppointmentCreate, Appointment
from app.models import Appointment as AppointmentModel
from app.database import SessionLocal

router = APIRouter()

@router.get("/", response_model=list[Appointment])
def get_appointments():
    db = SessionLocal()
    appointments = db.query(AppointmentModel).all()
    db.close()
    return appointments

@router.post("/", response_model=Appointment)
def create_appointment(appointment: AppointmentCreate):
    db = SessionLocal()
    db_appointment = AppointmentModel(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        date=appointment.date,
        time=appointment.time
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    db.close()
    return db_appointment

@router.put("/{id}", response_model=Appointment)
def update_appointment(id: int, appointment: AppointmentCreate):
    db = SessionLocal()
    db_appointment = db.query(AppointmentModel).filter(AppointmentModel.id == id).first()
    if not db_appointment:
        db.close()
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    db_appointment.patient_id = appointment.patient_id
    db_appointment.doctor_id = appointment.doctor_id
    db_appointment.date = appointment.date
    db_appointment.time = appointment.time
    db.commit()
    db.refresh(db_appointment)
    db.close()
    return db_appointment

@router.delete("/{id}")
def delete_appointment(id: int):
    db = SessionLocal()
    db_appointment = db.query(AppointmentModel).filter(AppointmentModel.id == id).first()
    if not db_appointment:
        db.close()
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    db.delete(db_appointment)
    db.commit()
    db.close()
    return {"message": "Consulta deletada com sucesso"}