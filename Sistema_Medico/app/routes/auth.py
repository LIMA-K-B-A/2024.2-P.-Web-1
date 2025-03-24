from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.core.security import (
    authenticate_user,
    create_access_token,
    get_current_user_from_token,
    verify_password
)
from app.schemas import Token, UsuarioLogin
from app.config import settings
from fastapi.templating import Jinja2Templates
from app.models import Usuario

router = APIRouter(prefix="/login", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """Rota para a página de login."""
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "title": "MedHub - Login"}
    )

@router.post("/")
async def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    """Rota de autenticação."""
    try:
        print(f"Tentando login com email: {email}")  # Log para debug
        
        # Busca o usuário pelo email
        db_usuario = db.query(Usuario).filter(Usuario.email == email).first()
        
        if not db_usuario:
            print(f"Usuário não encontrado: {email}")  # Log para debug
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Email ou senha incorretos"}
            )

        print(f"Usuário encontrado: {db_usuario.nome}")  # Log para debug
        print(f"Senha armazenada: {db_usuario.senha}")  # Log para debug
        
        # Verifica a senha
        if not verify_password(senha, db_usuario.senha):
            print(f"Senha incorreta para usuário: {email}")  # Log para debug
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Email ou senha incorretos"}
            )
        
        print(f"Senha correta para usuário: {email}")  # Log para debug
        
        # Cria o token de acesso
        access_token = create_access_token(data={"sub": str(db_usuario.id)})
        
        # Retorna o token e redireciona para a página inicial
        response = RedirectResponse(url="/home", status_code=status.HTTP_302_FOUND)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True,
            samesite="lax"
        )
        return response
    except Exception as e:
        print(f"Erro no login: {str(e)}")  # Log do erro para debug
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Erro ao fazer login. Tente novamente."}
        )

@router.get("/logout")
async def logout():
    """Rota de logout."""
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response

@router.get("/me")
async def read_users_me(request: Request, db: Session = Depends(get_db)):
    """Obtém informações do usuário atual."""
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não autenticado"
            )
        
        user = get_current_user_from_token(token, db)
        return {
            "id": user.id,
            "nome": user.nome,
            "email": user.email,
            "tipo_usuario": user.tipo_usuario
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
