from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import patient, doctor, appointment
from app.database import engine, Base

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gerenciamento de Consultas Médicas")

# Incluir as rotas
app.include_router(patient.router, prefix="/patients", tags=["Patients"])
app.include_router(doctor.router, prefix="/doctors", tags=["Doctors"])
app.include_router(appointment.router, prefix="/appointments", tags=["Appointments"])

# Configuração de templates
templates = Jinja2Templates(directory="templates")

# Configurar arquivos estáticos (CSS, JS, imagens, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})