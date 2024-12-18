# 🏥 **Gerenciamento de Consultas Médicas com FastAPI** 🏥

Este projeto implementa uma **API RESTful** para o **gerenciamento de consultas médicas**, permitindo o cadastro de **pacientes**, **médicos** e **consultas**, com operações completas de **CRUD** (Create, Read, Update, Delete) utilizando o framework **FastAPI**.

A API é desenvolvida para gerenciar informações de **pacientes**, **médicos** e **consultas** de maneira simples e eficiente, facilitando o controle dessas informações em uma aplicação de saúde.

## 📋 **Problema Resolvido**
Este sistema visa resolver o problema de gerenciamento de dados médicos, facilitando o controle de pacientes, médicos e consultas em um ambiente médico. Ele oferece uma forma simples de registrar, atualizar e consultar informações essenciais sobre pacientes, médicos e consultas médicas.

### **Principais funcionalidades:**
- **Cadastro de pacientes**: Adicionar, listar, atualizar e remover pacientes.
- **Cadastro de médicos**: Adicionar, listar, atualizar e remover médicos.
- **Gestão de consultas médicas**: Agendar, listar, atualizar e cancelar consultas.

## 🛠 **Requisitos Técnicos**

### **FastAPI**:
- Framework utilizado para criar a API.
- Implementação dos métodos HTTP **GET**, **POST**, **PUT**, **DELETE** para gerenciar pacientes, médicos e consultas.
- Armazenamento em memória utilizando listas (simulação de um banco de dados simples).

### **Postman**:
- Documentação completa das rotas da API, incluindo exemplos de requisições.
- Teste de todas as rotas da API para garantir o funcionamento adequado.

### **GitHub**:
- Repositório no GitHub com uma estrutura de arquivos clara e bem organizada.
- Arquivo `README.md` explicativo, com instruções de uso e exemplos de requisições.

## 🚀 **Instalação e Execução**

### 1️⃣ **Clone o Repositório**
Primeiro, clone o repositório para o seu computador:
```bash

### **2️⃣ Crie e Ative o Ambiente Virtual**

É altamente recomendado criar um ambiente virtual para instalar as dependências:
```bash
python3 -m venv venv
source venv/bin/activate  # Para Linux/MacOS
venv\Scripts\activate     # Para Windows
```

---

### **3️⃣ Instale as Dependências**

Com o ambiente virtual ativado, instale as dependências:
```bash
pip install -r requirements.txt
```

---

### **4️⃣ Execute a API**

Agora, inicie o servidor com o **Uvicorn**:
```bash
uvicorn main:app --reload
```

A API estará disponível em: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

---

## 📑 **Documentação no Postman**

A coleção do **Postman** contendo todas as rotas da API está disponível no repositório. Para importar a coleção no Postman:

1. Baixe o arquivo de coleção do **Postman**.
2. No **Postman**, clique em **"Import"** no canto superior esquerdo.
3. Selecione **"Upload Files"** e escolha o arquivo **`gerenciamento-consultas-medicas.postman_collection.json`**.
4. Agora você terá acesso a todas as rotas da API para testar e interagir diretamente com a documentação interativa.

---

## 🔨 **Exemplos de Rotas**

### **Pacientes**
- **GET `/patients`**: Retorna todos os pacientes.
  ```bash
  curl -X GET http://127.0.0.1:8000/patients
  ```

- **POST `/patients`**: Adiciona um novo paciente.
  Corpo (JSON):
  ```json
  {
    "name": "João Silva",
    "age": 30,
    "condition": "Hipertensão"
  }
  ```

- **PUT `/patients/{id}`**: Atualiza um paciente existente.

- **DELETE `/patients/{id}`**: Remove um paciente.

---

### **Médicos**
- **GET `/doctors`**: Retorna todos os médicos.

- **POST `/doctors`**: Adiciona um novo médico.
  Corpo (JSON):
  ```json
  {
    "name": "Dr. João",
    "specialty": "Cardiologia",
    "years_of_experience": 10
  }
  ```

---

### **Consultas**
- **GET `/appointments`**: Retorna todas as consultas agendadas.

- **POST `/appointments`**: Agenda uma nova consulta.
  Corpo (JSON):
  ```json
  {
    "patient_id": 1,
    "doctor_id": 1,
    "date": "2024-12-10",
    "time": "10:30"
  }
  ```

---

## 📥 **Como Contribuir**

Se você deseja contribuir para o projeto, siga as etapas abaixo:

1. Faça um **fork** do repositório.
2. Crie uma nova branch com a sua feature:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça o commit das suas alterações:
   ```bash
   git commit -m "Adiciona nova funcionalidade"
   ```
4. Envie para a sua branch remota:
   ```bash
   git push origin minha-feature
   ```
5. Abra um **Pull Request** no repositório original.

---
