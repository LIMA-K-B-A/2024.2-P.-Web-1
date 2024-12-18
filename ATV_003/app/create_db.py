from app.database import engine
from app.models import Base

# Criando as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
