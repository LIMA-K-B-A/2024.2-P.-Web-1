# app/main.py
from fastapi import FastAPI
from app.routes import auth, dashboard
from app.database import engine, Base

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Configuração do FastAPI
app = FastAPI(title="Medical Management System")

# Inclusão das rotas
app.include_router(auth.router)
app.include_router(dashboard.router)

# Rota inicial
@app.get("/")
async def home():
    return {"message": "Welcome to the Medical Management System"}
