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
git clone https://github.com/seu-usuario/gerenciamento-consultas-medicas.git
cd gerenciamento-consultas-medicas

2️⃣ Crie e Ative o Ambiente Virtual

É recomendado criar um ambiente virtual para instalar as dependências:

python3 -m venv venv
source venv/bin/activate  # Para Linux/MacOS
venv\Scripts\activate     # Para Windows

3️⃣ Instale as Dependências

Com o ambiente virtual ativado, instale as dependências:

pip install -r requirements.txt

4️⃣ Execute a API

Agora, inicie o servidor com o Uvicorn:

uvicorn main:app --reload

A API estará disponível em: http://127.0.0.1:8000
5️⃣ Documentação Interativa

O FastAPI já fornece uma documentação interativa com a Swagger:

    Documentação de uso: http://127.0.0.1:8000/docs
    Esquema OpenAPI: http://127.0.0.1:8000/openapi.json

🧑‍💻 Testando a API no Postman
Passo 1: Criação da Coleção no Postman

    Abra o Postman e crie uma nova Coleção chamada "Gerenciamento de Consultas Médicas".
    Adicione as rotas de Pacientes, Médicos e Consultas à coleção, com os métodos GET, POST, PUT e DELETE.

Passo 2: Exemplos de Requisição
1. Pacientes

    GET /patients: Retorna todos os pacientes.
        Método: GET
        URL: http://127.0.0.1:8000/patients

    POST /patients: Adiciona um novo paciente.
        Método: POST
        Corpo (JSON):

    {
      "name": "João Silva",
      "age": 30,
      "condition": "Hipertensão"
    }

PUT /patients/{patient_id}: Atualiza os dados de um paciente.

    Método: PUT
    URL: http://127.0.0.1:8000/patients/1
    Corpo (JSON):

        {
          "name": "João Silva",
          "age": 31,
          "condition": "Hipertensão moderada"
        }

    DELETE /patients/{patient_id}: Remove um paciente.
        Método: DELETE
        URL: http://127.0.0.1:8000/patients/1

2. Médicos

    GET /doctors: Retorna todos os médicos.
        Método: GET
        URL: http://127.0.0.1:8000/doctors

    POST /doctors: Adiciona um novo médico.
        Método: POST
        Corpo (JSON):

    {
      "name": "Dr. João",
      "specialty": "Cardiologia",
      "years_of_experience": 10
    }

PUT /doctors/{doctor_id}: Atualiza os dados de um médico.

    Método: PUT
    URL: http://127.0.0.1:8000/doctors/1
    Corpo (JSON):

        {
          "name": "Dr. João",
          "specialty": "Cardiologia",
          "years_of_experience": 12
        }

    DELETE /doctors/{doctor_id}: Remove um médico.
        Método: DELETE
        URL: http://127.0.0.1:8000/doctors/1

3. Consultas

    GET /appointments: Retorna todas as consultas.
        Método: GET
        URL: http://127.0.0.1:8000/appointments

    POST /appointments: Agendar uma nova consulta.
        Método: POST
        Corpo (JSON):

    {
      "patient_id": 1,
      "doctor_id": 1,
      "date": "2024-12-10",
      "time": "10:30"
    }

PUT /appointments/{appointment_id}: Atualiza uma consulta existente.

    Método: PUT
    URL: http://127.0.0.1:8000/appointments/1
    Corpo (JSON):

        {
          "patient_id": 1,
          "doctor_id": 1,
          "date": "2024-12-15",
          "time": "14:00"
        }

    DELETE /appointments/{appointment_id}: Remove uma consulta.
        Método: DELETE
        URL: http://127.0.0.1:8000/appointments/1

🛠 Tecnologias Utilizadas

    FastAPI: Framework para criar APIs RESTful de forma rápida e eficiente.
    Uvicorn: Servidor ASGI para rodar a aplicação FastAPI.
    Pydantic: Para validação de dados de entrada e saída.
    Postman: Para testar e documentar as rotas da API.