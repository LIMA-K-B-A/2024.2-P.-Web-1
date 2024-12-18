from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados (mude conforme sua necessidade)
DATABASE_URL = "sqlite:///./test.db"  # Exemplo usando SQLite, mas você pode usar outros bancos (PostgreSQL, MySQL, etc.)

# Criando o engine de conexão
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Para SQLite

# Criando a base de dados
Base = declarative_base()

# Criando o session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter a sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()