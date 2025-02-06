from fastapi import FastAPI, Depends, HTTPException, status, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.routes import doctor, patient, appointment
from app.auth import get_current_user, verify_jwt_token

# Inicializando o app FastAPI
app = FastAPI()

# Carregar templates
templates = Jinja2Templates(directory="app/templates")

# Criação do banco de dados
database.Base.metadata.create_all(bind=database.engine)

# Rotas
app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(appointment.router)