# main.py
from fastapi import FastAPI
from app.router import medicos, pacientes, consultas

app = FastAPI()

app.include_router(medicos.router)
app.include_router(pacientes.router)
app.include_router(consultas.router)