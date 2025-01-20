from fastapi import FastAPI
from app.routes import patient, doctor, appointment
from app.database import engine, Base

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gerenciamento de Consultas Médicas")

# Incluir as rotas
app.include_router(patient.router, prefix="/patients", tags=["Patients"])
app.include_router(doctor.router, prefix="/doctors", tags=["Doctors"])
app.include_router(appointment.router, prefix="/appointments", tags=["Appointments"])

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Bem-vindo à API de Gerenciamento de Consultas Médicas!",
        "docs_url": "http://127.0.0.1:8000/docs",
    }