from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from app.models import Usuario, TipoUsuario
from app.schemas import UsuarioCreate, UsuarioOut, UsuarioUpdate
from app.database import get_db
from app.core.security import get_password_hash, get_current_user_from_token

router = APIRouter(prefix="/cadastro", tags=["cadastro"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def register_page(request: Request):
    """Rota para a página de registro."""
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "title": "MedHub - Cadastro"}
    )

@router.post("/")
async def register(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    tipo_usuario: str = Form(...),
    db: Session = Depends(get_db)
):
    """Rota para registro de usuário."""
    try:
        # Verifica se o email já existe
        db_usuario = db.query(Usuario).filter(Usuario.email == email).first()
        if db_usuario:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Email já cadastrado"}
            )

        # Cria hash da senha
        hashed_password = get_password_hash(senha)

        # Cria novo usuário
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=hashed_password,
            tipo_usuario=TipoUsuario(tipo_usuario)
        )

        # Adiciona ao banco de dados
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        # Retorna sucesso
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"detail": "Usuário cadastrado com sucesso"}
        )

    except Exception as e:
        db.rollback()
        print(f"Erro no registro: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Erro ao cadastrar usuário. Tente novamente."}
        )

@router.get("/users/{user_id}", response_model=UsuarioOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtém um usuário pelo ID."""
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.get("/users", response_model=List[UsuarioOut])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Lista todos os usuários."""
    return db.query(Usuario).offset(skip).limit(limit).all()

@router.put("/users/{user_id}", response_model=UsuarioOut)
def update_user(user_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    """Atualiza um usuário."""
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Atualiza os campos
    if usuario.nome:
        db_user.nome = usuario.nome
    if usuario.email:
        db_user.email = usuario.email
    if usuario.tipo_usuario:
        db_user.tipo_usuario = usuario.tipo_usuario
    if usuario.senha:
        db_user.senha = get_password_hash(usuario.senha)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Deleta um usuário."""
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(user)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}

@router.get("/me/{token}", response_model=UsuarioOut)
def read_current_user(token: str, db: Session = Depends(get_db)):
    """Obtém o usuário atual a partir do token."""
    return get_current_user_from_token(token, db)
