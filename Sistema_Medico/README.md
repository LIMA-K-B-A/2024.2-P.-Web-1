# MedHub - Sistema de Gestão Médica

O MedHub é um sistema web moderno para gestão de consultas médicas, desenvolvido com FastAPI e PostgreSQL. O sistema oferece uma interface intuitiva e responsiva para gerenciar médicos, pacientes e consultas.

## Funcionalidades

- **Gestão de Consultas**
  - Agendamento de consultas
  - Histórico de consultas
  - Status de consultas (agendada, realizada, cancelada)
  - Filtros e busca

- **Gestão de Médicos**
  - Cadastro de médicos
  - Especialidades
  - Horários de atendimento
  - Histórico de atendimentos

- **Gestão de Pacientes**
  - Cadastro de pacientes
  - Histórico médico
  - Prontuário digital
  - Histórico de consultas

- **Dashboard**
  - Estatísticas gerais
  - Gráficos de atendimentos
  - Próximas consultas
  - Alertas e notificações

## Tecnologias Utilizadas

- **Backend**
  - FastAPI
  - SQLAlchemy
  - PostgreSQL
  - JWT Authentication
  - Pydantic

- **Frontend**
  - HTML5
  - CSS3 (com variáveis CSS)
  - JavaScript (Vanilla)
  - Font Awesome
  - Google Fonts

## Instalação

1. Clone o repositório:
   ```bash
git clone https://github.com/seu-usuario/medhub.git
cd medhub
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute as migrações do banco de dados:
   ```bash
alembic upgrade head
```

6. Inicie o servidor:
   ```bash
uvicorn app.main:app --reload
```

## Estrutura do Projeto

```
medhub/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   └── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── consulta.py
│   │   ├── medico.py
│   │   └── paciente.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── img/
│   │       └── favicon.svg
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── home.html
│   │   ├── consulta.html
│   │   ├── medico.html
│   │   ├── paciente.html
│   │   └── perfil.html
│   └── main.py
├── alembic/
│   ├── versions/
│   └── alembic.ini
├── tests/
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Segurança

- Autenticação JWT
- Senhas criptografadas com bcrypt
- Validação de dados com Pydantic
- Proteção contra CSRF
- Sanitização de inputs

## Responsividade

O sistema é totalmente responsivo e funciona bem em:
- Desktops
- Tablets
- Smartphones

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autores

- Seu Nome - [GitHub](https://github.com/seu-usuario)

## Agradecimentos

- FastAPI
- SQLAlchemy
- PostgreSQL
- Font Awesome
- Google Fonts
- E todos os outros projetos open-source utilizados
