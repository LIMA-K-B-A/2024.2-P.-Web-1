from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserCreate, UserLogin
from ..crud import create_user, get_user_by_email
from ..dependencies import get_current_user, oauth2_scheme
from jose import jwt
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.post("/register")
async def register_user(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    user_data = {
        "email": form_data.get("email"),
        "password": form_data.get("password"),
        "full_name": form_data.get("full_name")
    }
    photo = form_data.get("photo")
    
    # Salvar a foto
    photo_path = f"static/uploads/{photo.filename}"
    with open(photo_path, "wb") as buffer:
        buffer.write(await photo.read())
    
    create_user(db, user_data, photo_path)
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.post("/login")
async def login_user(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    user = get_user_by_email(db, form_data.get("email"))
    
    if not user or not pwd_context.verify(form_data.get("password"), user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    token_data = {
        "sub": user.email,
        "name": user.full_name,
        "photo": user.photo
    }
    
    token = jwt.encode(token_data, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return response