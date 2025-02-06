# app/routes/dashboard.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.utils import verify_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função para verificar o token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

# Rota protegida
@router.get("/dashboard")
async def dashboard(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user['sub']}!"}
