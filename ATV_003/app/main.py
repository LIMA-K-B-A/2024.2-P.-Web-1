from fastapi import FastAPI
from app.database import engine, Base
from app.routes import patient, doctor, appointment

app = FastAPI(title="Gerenciamento de Consultas Médicas")

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Rotas
app.include_router(patient.router, prefix="/patients", tags=["Patients"])
app.include_router(doctor.router, prefix="/doctors", tags=["Doctors"])
app.include_router(appointment.router, prefix="/appointments", tags=["Appointments"])
