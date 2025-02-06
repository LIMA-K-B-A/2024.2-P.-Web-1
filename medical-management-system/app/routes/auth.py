from fastapi import APIRouter, Depends, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin, Token

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

SECRET_KEY = "chave-secreta-super-segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
    user = db.query(User).filter(User.email == email).first()
    return user

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/token", response_class=HTMLResponse)
async def login_for_access_token(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    user = db.query(User).filter(User.email == form_data["username"]).first()
    if not user or not verify_password(form_data["password"], user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciais inválidas"})
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    profile_picture: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    hashed_password = get_password_hash(password)
    profile_picture_data = await profile_picture.read() if profile_picture else None
    user = User(email=email, hashed_password=hashed_password, role=role, profile_picture=profile_picture_data)
    db.add(user)
    db.commit()
    return RedirectResponse(url="/login", status_code=303)

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login")
    if current_user.role == "admin":
        return templates.TemplateResponse("dashboard/admin.html", {"request": request})
    elif current_user.role == "doctor":
        return templates.TemplateResponse("dashboard/doctor.html", {"request": request})
    else:
        return templates.TemplateResponse("dashboard/patient.html", {"request": request})