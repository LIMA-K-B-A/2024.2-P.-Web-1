from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings  # Importando as variáveis de ambiente

# Configurando a URL de conexão com o banco de dados a partir do arquivo de configurações
DATABASE_URL = settings.DATABASE_URL

# Criação do engine com a URL do banco de dados e configuração do encoding
engine = create_engine(DATABASE_URL, connect_args={"options": "-c client_encoding=UTF8"})

# Criando a sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarando a base para as tabelas
Base = declarative_base()

# Função para criar as tabelas
def create_tables():
    Base.metadata.create_all(bind=engine)
