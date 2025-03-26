from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, get_db
from app.routes import (
    register_router,
    auth_router,
    consulta_router,
    medico_router,
    paciente_router,
    usuario
)
from app.core.security import get_current_user_from_token
from sqlalchemy.orm import Session
from app.models import Usuario
import os

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="MedHub",
    description="Sistema de Gerenciamento de Consultas Médicas",
    version="1.0.0"
)

# Configuração de templates e arquivos estáticos
templates = Jinja2Templates(directory="app/templates")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Lista de rotas públicas
public_routes = [
    "/",
    "/login",
    "/login/",
    "/cadastro",
    "/cadastro/",
    "/static",
    "/favicon.ico",
    "/static/img/favicon.svg",
    "/static/css/style.css",
    "/static/js/main.js"
]

# Middleware de autenticação
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    path = request.url.path
    
    # Verifica se a rota é pública
    if any(path.startswith(route) for route in public_routes):
        return await call_next(request)
    
    # Verifica se é um arquivo estático
    if path.startswith("/static/") or path.endswith((".ico", ".css", ".js", ".svg", ".png", ".jpg", ".jpeg")):
        return await call_next(request)
    
    # Verifica se o usuário está autenticado
    try:
        token = request.cookies.get("access_token")
        if not token:
            return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
        # Remove o prefixo 'Bearer ' se existir
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        
        db = next(get_db())
        user = get_current_user_from_token(token, db)
        if not user:
            return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
        # Adiciona o usuário ao request state
        request.state.user = user
        
        response = await call_next(request)
        return response
        
    except Exception as e:
        print(f"Erro na autenticação: {str(e)}")
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

# Inclui os routers
app.include_router(auth_router)
app.include_router(register_router)
app.include_router(consulta_router, prefix="/consultas")
app.include_router(medico_router, prefix="/medicos")
app.include_router(paciente_router, prefix="/pacientes")
app.include_router(usuario.router, prefix="/usuarios", tags=["usuarios"])

# Rota específica para o favicon
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/img/favicon.svg", media_type="image/svg+xml")

# Rota principal
@app.get("/")
async def root():
    """Rota raiz que redireciona para a página de login."""
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

# Função para obter o usuário atual
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Não autenticado")
    
    user = get_current_user_from_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado")
    
    return user

# Rotas protegidas
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, current_user = Depends(get_current_user)):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "MedHub - Dashboard",
            "user": current_user
        }
    )

@app.get("/listaMedicos", response_class=HTMLResponse)
async def lista_medicos(request: Request, current_user = Depends(get_current_user)):
    return templates.TemplateResponse(
        "medicos.html",
        {
            "request": request,
            "title": "MedHub - Médicos",
            "user": current_user
        }
    )

@app.get("/listaPacientes", response_class=HTMLResponse)
async def lista_pacientes(request: Request, current_user = Depends(get_current_user)):
    return templates.TemplateResponse(
        "pacientes.html",
        {
            "request": request,
            "title": "MedHub - Pacientes",
            "user": current_user
        }
    )

@app.get("/listaConsultas", response_class=HTMLResponse)
async def lista_consultas(request: Request, current_user = Depends(get_current_user)):
    return templates.TemplateResponse(
        "consulta.html",
        {
            "request": request,
            "title": "MedHub - Consultas",
            "user": current_user
        }
    )

@app.get("/perfil", response_class=HTMLResponse)
async def perfil(request: Request, current_user = Depends(get_current_user)):
    return templates.TemplateResponse(
        "perfil.html",
        {
            "request": request,
            "title": "MedHub - Perfil",
            "user": current_user
        }
    )

@app.put("/perfil/atualizar")
async def atualizar_perfil(
    request: Request, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        # Obter dados do corpo da requisição
        dados = await request.json()
        nome = dados.get("nome")
        email = dados.get("email")
        
        if not nome or not email:
            raise HTTPException(status_code=400, detail="Nome e email são obrigatórios")
        
        # Verificar se o email já está sendo usado por outro usuário
        usuario_existente = db.query(Usuario).filter(Usuario.email == email, Usuario.id != current_user.id).first()
        if usuario_existente:
            raise HTTPException(status_code=400, detail="Email já está em uso")
        
        # Atualizar os dados do usuário
        current_user.nome = nome
        current_user.email = email
        db.commit()
        
        return {"message": "Perfil atualizado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar perfil: {str(e)}")

@app.put("/perfil/senha")
async def atualizar_senha(
    request: Request, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        from app.core.security import verify_password, get_password_hash
        
        # Obter dados do corpo da requisição
        dados = await request.json()
        senha_atual = dados.get("senha_atual")
        nova_senha = dados.get("nova_senha")
        
        if not senha_atual or not nova_senha:
            raise HTTPException(status_code=400, detail="Senha atual e nova senha são obrigatórias")
        
        # Verificar se a senha atual está correta
        if not verify_password(senha_atual, current_user.senha):
            raise HTTPException(status_code=400, detail="Senha atual incorreta")
        
        # Atualizar a senha
        current_user.senha = get_password_hash(nova_senha)
        db.commit()
        
        return {"message": "Senha atualizada com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar senha: {str(e)}")

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response