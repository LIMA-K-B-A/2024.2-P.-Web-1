from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Bem-vindo à API de Gerenciamento de Consultas Médicas!",
        "docs_url": "http://127.0.0.1:8000/docs",
        "openapi_url": "http://127.0.0.1:8000/openapi.json"
    }

# Modelos Pydantic para validação de dados
class Patient(BaseModel):
    name: str
    age: int
    condition: str

class Doctor(BaseModel):
    name: str
    specialty: str
    years_of_experience: int

class Appointment(BaseModel):
    patient_id: int
    doctor_id: int
    date: str  # Pode ser uma string com formato de data 'YYYY-MM-DD'
    time: str  # Horário da consulta 'HH:MM'

# Dados em memória (simulação)
patients = []
doctors = []
appointments = []

# --- Pacientes ---
@app.get("/patients", response_model=List[Patient], tags=["Pacientes"])
def get_patients():
    """Retorna todos os pacientes cadastrados."""
    return patients

@app.post("/patients", response_model=Patient, tags=["Pacientes"])
def add_patient(patient: Patient):
    """Adiciona um novo paciente."""
    patient_dict = patient.dict()
    patient_dict['id'] = len(patients) + 1
    patients.append(patient_dict)
    return patient_dict

@app.put("/patients/{patient_id}", response_model=Patient, tags=["Pacientes"])
def update_patient(patient_id: int, updated_patient: Patient):
    """Atualiza os dados de um paciente específico."""
    for patient in patients:
        if patient["id"] == patient_id:
            patient.update(updated_patient.dict())
            return patient
    raise HTTPException(status_code=404, detail="Paciente não encontrado")

@app.delete("/patients/{patient_id}", response_model=dict, tags=["Pacientes"])
def delete_patient(patient_id: int):
    """Remove um paciente com base no ID."""
    global patients
    patients = [p for p in patients if p["id"] != patient_id]
    return {"message": "Paciente deletado com sucesso"}

# --- Médicos ---
@app.get("/doctors", response_model=List[Doctor], tags=["Médicos"])
def get_doctors():
    """Retorna todos os médicos cadastrados."""
    return doctors

@app.post("/doctors", response_model=Doctor, tags=["Médicos"])
def add_doctor(doctor: Doctor):
    """Adiciona um novo médico."""
    doctor_dict = doctor.dict()
    doctor_dict['id'] = len(doctors) + 1
    doctors.append(doctor_dict)
    return doctor_dict

@app.put("/doctors/{doctor_id}", response_model=Doctor, tags=["Médicos"])
def update_doctor(doctor_id: int, updated_doctor: Doctor):
    """Atualiza os dados de um médico específico."""
    for doctor in doctors:
        if doctor["id"] == doctor_id:
            doctor.update(updated_doctor.dict())
            return doctor
    raise HTTPException(status_code=404, detail="Médico não encontrado")

@app.delete("/doctors/{doctor_id}", response_model=dict, tags=["Médicos"])
def delete_doctor(doctor_id: int):
    """Remove um médico com base no ID."""
    global doctors
    doctors = [d for d in doctors if d["id"] != doctor_id]
    return {"message": "Médico deletado com sucesso"}

# --- Consultas ---
@app.get("/appointments", response_model=List[Appointment], tags=["Consultas"])
def get_appointments():
    """Retorna todas as consultas agendadas."""
    return appointments

@app.post("/appointments", response_model=Appointment, tags=["Consultas"])
def add_appointment(appointment: Appointment):
    """Agenda uma nova consulta."""
    # Verifica se o paciente e o médico existem
    if not any(patient["id"] == appointment.patient_id for patient in patients):
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if not any(doctor["id"] == appointment.doctor_id for doctor in doctors):
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    appointment_dict = appointment.dict()
    appointment_dict['id'] = len(appointments) + 1
    appointments.append(appointment_dict)
    return appointment_dict

@app.put("/appointments/{appointment_id}", response_model=Appointment, tags=["Consultas"])
def update_appointment(appointment_id: int, updated_appointment: Appointment):
    """Atualiza os dados de uma consulta específica."""
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            appointment.update(updated_appointment.dict())
            return appointment
    raise HTTPException(status_code=404, detail="Consulta não encontrada")

@app.delete("/appointments/{appointment_id}", response_model=dict, tags=["Consultas"])
def delete_appointment(appointment_id: int):
    """Remove uma consulta com base no ID."""
    global appointments
    appointments = [a for a in appointments if a["id"] != appointment_id]
    return {"message": "Consulta deletada com sucesso"}