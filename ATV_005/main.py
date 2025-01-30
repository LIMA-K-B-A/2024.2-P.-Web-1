import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import (
    FastAPI, 
    Depends, 
    HTTPException, 
    status, 
    UploadFile, 
    File,
    Request,
    Form
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI()

# Configurações
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuração de pastas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Banco de dados temporário
fake_users_db = {}

# Modelos
class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    photo_url: Optional[str] = None

class UserInDB(User):
    hashed_password: str
    reset_token: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

# Configurações de segurança
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Funções auxiliares
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    user = fake_users_db.get(username)
    return user

# Rotas de autenticação
@app.post("/token")
async def login_for_access_token(response: RedirectResponse, 
                               form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        return RedirectResponse("/login?error=1", status_code=status.HTTP_303_SEE_OTHER)
    
    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/protected", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.post("/register")
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    photo: UploadFile = File(None)
):
    if username in fake_users_db:
        return RedirectResponse("/register?error=1", status_code=303)
    
    hashed_password = get_password_hash(password)
    photo_url = None
    
    if photo:
        upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, photo.filename)
        with open(file_path, "wb") as f:
            f.write(await photo.read())
        photo_url = f"/static/uploads/{photo.filename}"
    
    fake_users_db[username] = UserInDB(
        username=username,
        email=email,
        hashed_password=hashed_password,
        photo_url=photo_url,
        reset_token=None
    )
    return RedirectResponse("/login?success=1", status_code=303)

@app.post("/forgot-password")
async def forgot_password(email: str = Form(...)):
    for user in fake_users_db.values():
        if user.email == email:
            reset_token = secrets.token_urlsafe()
            user.reset_token = reset_token
            return RedirectResponse(f"/reset-password?token={reset_token}", status_code=303)
    return RedirectResponse("/forgot-password?error=1", status_code=303)

@app.post("/reset-password")
async def reset_password(
    token: str = Form(...),
    new_password: str = Form(...)
):
    for user in fake_users_db.values():
        if user.reset_token == token:
            user.hashed_password = get_password_hash(new_password)
            user.reset_token = None
            return RedirectResponse("/login?reset=1", status_code=303)
    return RedirectResponse("/reset-password?error=1", status_code=303)

# Rotas de páginas
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = await get_current_user(request)
    if user:
        return RedirectResponse("/protected")
    return RedirectResponse("/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot-password.html", {"request": request})

@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str):
    return templates.TemplateResponse("reset-password.html", {
        "request": request,
        "token": token
    })

@app.get("/protected", response_class=HTMLResponse)
async def protected_page(request: Request):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("protected.html", {
        "request": request,
        "user": user
    })

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)