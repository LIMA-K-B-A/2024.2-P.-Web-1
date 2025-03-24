from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configurações do banco de dados
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    DATABASE_PORT: str
    
    # Configurações de segurança
    SECRET_KEY: str = "sua_chave_super_secreta_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configurações de email
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None
    
    # Configurações da aplicação
    APP_NAME: str = "MedHub"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings() 