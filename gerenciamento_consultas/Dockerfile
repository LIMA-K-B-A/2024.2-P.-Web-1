# Imagem base
FROM python:3.10-slim

# Definir diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos do projeto para o contêiner
COPY . .

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]