# app/utils.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Instância do CryptContext para criptografia de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Chave secreta para JWT
SECRET_KEY = "5e684e9d8cd8b97c32d8b9466e1db6d30684b3037c4a3edb92ac59deab16f5f1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Função para criar hash de senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar o hash de uma senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar o token de acesso (JWT)
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar o token de acesso (JWT)
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
