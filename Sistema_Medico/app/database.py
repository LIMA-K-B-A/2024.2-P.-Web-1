from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o PostgreSQL no Docker
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1301@db:5432/medhub"

# Criar o engine do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criar a classe SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar a classe Base
Base = declarative_base()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
