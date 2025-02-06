from sqlalchemy.orm import Session
from .models import User, Doctor, Patient, Appointment
from passlib.context import CryptContext
import os
from datetime import datetime
from . import schemas  # Certifique-se de importar seus schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funções CRUD para Usuário
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, photo_path: str):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        photo=photo_path
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate, photo_path: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.full_name = user.full_name
        db_user.email = user.email
        db_user.photo = photo_path
        if user.password:
            db_user.hashed_password = pwd_context.hash(user.password)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# Funções CRUD para Médico
def get_doctor(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()

def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = Doctor(
        full_name=doctor.full_name,
        email=doctor.email,
        phone=doctor.phone,
        specialty=doctor.specialty
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def update_doctor(db: Session, doctor_id: int, doctor: schemas.DoctorUpdate):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if db_doctor:
        db_doctor.full_name = doctor.full_name
        db_doctor.email = doctor.email
        db_doctor.phone = doctor.phone
        db_doctor.specialty = doctor.specialty
        db.commit()
        db.refresh(db_doctor)
    return db_doctor

def delete_doctor(db: Session, doctor_id: int):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if db_doctor:
        db.delete(db_doctor)
        db.commit()
    return db_doctor


# Funções CRUD para Paciente
def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = Patient(
        full_name=patient.full_name,
        email=patient.email,
        phone=patient.phone,
        birth_date=patient.birth_date
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def update_patient(db: Session, patient_id: int, patient: schemas.PatientUpdate):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient:
        db_patient.full_name = patient.full_name
        db_patient.email = patient.email
        db_patient.phone = patient.phone
        db_patient.birth_date = patient.birth_date
        db.commit()
        db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient:
        db.delete(db_patient)
        db.commit()
    return db_patient


# Funções CRUD para Consulta Médica
def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def create_appointment(db: Session, appointment: schemas.AppointmentCreate, patient_id: int, doctor_id: int):
    db_appointment = Appointment(
        appointment_time=appointment.appointment_time,
        patient_id=patient_id,
        doctor_id=doctor_id,
        reason=appointment.reason
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def update_appointment(db: Session, appointment_id: int, appointment: schemas.AppointmentUpdate):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if db_appointment:
        db_appointment.appointment_time = appointment.appointment_time
        db_appointment.reason = appointment.reason
        db.commit()
        db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
    return db_appointment
