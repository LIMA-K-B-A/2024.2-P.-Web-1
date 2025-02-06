import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtendo a URL do banco de dados a partir do .env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:1301@localhost:5432/consultas_medicas")

# Configuração do banco de dados
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Função para criar o banco de dados
def create_db():
    Base.metadata.create_all(bind=engine)
