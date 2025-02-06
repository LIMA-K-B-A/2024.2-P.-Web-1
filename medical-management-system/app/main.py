# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import auth, patient, doctor, appointment
from app.database import engine, Base

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Configuração do FastAPI
app = FastAPI(title="Medical Management System")

# Configuração do diretório de arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configuração do Jinja2 para templates
templates = Jinja2Templates(directory="app/templates")

# Inclusão das rotas
app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointment.router)

# Rota inicial
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})