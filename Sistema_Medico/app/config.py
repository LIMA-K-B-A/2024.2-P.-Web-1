from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Settings(BaseSettings):
    # Configurações do banco de dados
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "1301")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "medhub")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")

    # Configurações de autenticação
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    class Config:
        env_file = ".env"

# Instanciando a classe para carregar as variáveis de ambiente
settings = Settings()
