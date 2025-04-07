# Use a imagem oficial do Python como base 
FROM python:3.11-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Instale as dependências necessárias para compilar o psycopg2 e o pg_isready
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instala as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Criar diretório de uploads
RUN mkdir -p app/static/uploads && chmod 777 app/static/uploads

# Expõe a porta 8000 (porta padrão do Uvicorn)
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
