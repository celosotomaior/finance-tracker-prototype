# 📦 Finance Tracker - Visão Geral do Projeto

## 🎯 Objetivo

Protótipo didático completo para aprender desenvolvimento full-stack em Python com:
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: Streamlit + Plotly
- **Arquitetura**: Organizada em camadas (models, schemas, services, routes)

---

## 📁 Estrutura Completa

```
finance-tracker/
├── README.md                    # Documentação completa
├── QUICKSTART.md                # Guia rápido de início
├── .gitignore                   # Arquivos a ignorar no Git
│
├── backend/                     # API FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # ⭐ Aplicação FastAPI principal
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py       # ⭐ Todos os endpoints REST
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── item.py         # ⭐ Modelo SQLAlchemy
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── item.py         # ⭐ Schemas Pydantic (validação)
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── item_service.py # ⭐ Lógica de negócio
│   │   │
│   │   └── db/
│   │       ├── __init__.py
│   │       └── database.py     # ⭐ Configuração do banco
│   │
│   ├── requirements.txt         # Dependências do backend
│   ├── .env.example            # Template de configuração
│   └── seed_data.py            # ⭐ Script para dados de exemplo
│
└── frontend/                    # Interface Streamlit
    ├── ui/
    │   ├── __init__.py
    │   └── app.py              # ⭐ Interface completa
    │
    └── requirements.txt         # Dependências do frontend
```

---

## 🔧 Tecnologias e Justificativas

### Backend

| Tecnologia | Versão | Por quê? |
|------------|--------|----------|
| **FastAPI** | 0.104.1 | Framework moderno, rápido, com validação automática e docs interativas |
| **SQLAlchemy** | 2.0.23 | ORM maduro e robusto (escolhido em vez de SQLModel por estabilidade) |
| **Pydantic** | 2.5.0 | Validação de dados poderosa, integrada ao FastAPI |
| **SQLite** | Built-in | Zero configuração, perfeito para protótipos |
| **Uvicorn** | 0.24.0 | Servidor ASGI de alta performance |

### Frontend

| Tecnologia | Versão | Por quê? |
|------------|--------|----------|
| **Streamlit** | 1.29.0 | Criação rápida de interfaces web sem HTML/CSS/JS |
| **Plotly** | 5.18.0 | Gráficos interativos bonitos e profissionais |
| **Pandas** | 2.1.3 | Manipulação de dados tabular |
| **Requests** | 2.31.0 | Comunicação HTTP com a API |

---

## 🏛️ Arquitetura em Camadas

```
┌─────────────────────────────────────────────────┐
│              FRONTEND (Streamlit)               │
│  - Interface visual                             │
│  - Formulários e tabelas                        │
│  - Gráficos com Plotly                         │
└────────────────┬────────────────────────────────┘
                 │ HTTP Requests
                 ▼
┌─────────────────────────────────────────────────┐
│           API ROUTES (FastAPI)                  │
│  - Endpoints REST                               │
│  - Validação de entrada (Pydantic)             │
│  - Tratamento de erros HTTP                    │
└────────────────┬────────────────────────────────┘
                 │ Dependency Injection
                 ▼
┌─────────────────────────────────────────────────┐
│              SERVICES (Lógica)                  │
│  - Regras de negócio                           │
│  - Cálculos e agregações                      │
│  - Orquestração                                │
└────────────────┬────────────────────────────────┘
                 │ ORM Queries
                 ▼
┌─────────────────────────────────────────────────┐
│           MODELS (SQLAlchemy)                   │
│  - Definição de tabelas                        │
│  - Relacionamentos                             │
│  - Mapeamento objeto-relacional                │
└────────────────┬────────────────────────────────┘
                 │ SQL
                 ▼
┌─────────────────────────────────────────────────┐
│            DATABASE (SQLite)                    │
│  - Armazenamento persistente                   │
│  - Arquivo: finance_tracker.db                 │
└─────────────────────────────────────────────────┘
```

### Vantagens desta Arquitetura

✅ **Separação de Responsabilidades**: Cada camada tem uma função clara  
✅ **Testabilidade**: Services podem ser testados isoladamente  
✅ **Manutenibilidade**: Mudanças em uma camada não afetam outras  
✅ **Escalabilidade**: Fácil adicionar novos recursos  
✅ **Reutilização**: Services podem ser usados por múltiplos endpoints  

---

## 📊 Funcionalidades Implementadas

### ✅ CRUD Completo

- **Create**: POST /api/items
- **Read**: GET /api/items, GET /api/items/{id}
- **Update**: PUT /api/items/{id}
- **Delete**: DELETE /api/items/{id}

### ✅ Filtros

- Por tipo (receita/despesa)
- Por categoria
- Por intervalo de datas
- Paginação (skip/limit)

### ✅ Análises

- Saldo total (receitas - despesas)
- Totais por categoria
- Totais por mês
- Gráficos de barras e pizza

### ✅ Validações

- Tipo obrigatório (income/expense)
- Categoria não vazia
- Valor positivo
- Data válida
- Descrição opcional (max 200 chars)

### ✅ UI Features

- Dashboard com métricas
- Formulário de cadastro
- Tabela de listagem
- Filtros na sidebar
- Feedback de loading/sucesso/erro
- Gráficos interativos

---

## 🧪 Exemplos de Uso

### Criar Item via API

```python
import requests

response = requests.post(
    "http://localhost:8000/api/items",
    json={
        "type": "expense",
        "category": "Alimentação",
        "amount": 150.50,
        "date": "2026-01-07",
        "description": "Supermercado"
    }
)
print(response.json())
```

### Buscar Itens com Filtros

```python
params = {
    "type": "expense",
    "date_from": "2026-01-01",
    "date_to": "2026-01-31"
}
response = requests.get("http://localhost:8000/api/items", params=params)
items = response.json()
```

### Calcular Saldo

```python
response = requests.get("http://localhost:8000/api/balance")
balance = response.json()["data"]
print(f"Saldo: R$ {balance['balance']:.2f}")
```

---

## 🎓 Conceitos Aprendidos

### 1. FastAPI

- ✅ Criação de rotas REST
- ✅ Dependency Injection (`Depends`)
- ✅ Validação automática com Pydantic
- ✅ Documentação automática (Swagger/ReDoc)
- ✅ Tratamento de erros HTTP
- ✅ CORS middleware
- ✅ Startup events

### 2. SQLAlchemy

- ✅ Modelos ORM
- ✅ Sessões e transações
- ✅ Queries com filtros
- ✅ Agregações (SUM, COUNT)
- ✅ Relacionamentos (preparado para expansão)

### 3. Pydantic

- ✅ Schemas de validação
- ✅ Field validators
- ✅ Enums
- ✅ Optional fields
- ✅ Model config

### 4. Streamlit

- ✅ Layouts (columns, sidebar)
- ✅ Formulários
- ✅ Dataframes interativos
- ✅ Métricas
- ✅ Session state
- ✅ API integration

### 5. Plotly

- ✅ Gráficos de barras
- ✅ Gráficos de pizza
- ✅ Customização de cores
- ✅ Integração com Streamlit

---

## 🚀 Próximos Passos

### Nível Intermediário

1. **Autenticação JWT**
   - Login/registro
   - Tokens seguros
   - Middleware de autenticação

2. **Testes**
   - Unitários (pytest)
   - Integração
   - Coverage

3. **Migrations**
   - Alembic
   - Versionamento do schema

### Nível Avançado

4. **Deploy**
   - Backend: Railway, Render
   - Frontend: Streamlit Cloud
   - Database: PostgreSQL

5. **Features**
   - Export CSV/Excel
   - Múltiplas contas
   - Categorias hierárquicas
   - Anexos (notas fiscais)
   - Relatórios PDF

6. **Otimizações**
   - Cache (Redis)
   - Background tasks (Celery)
   - Rate limiting
   - Pagination melhorada

---

## 📚 Recursos de Aprendizado

### Documentação Oficial

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Streamlit](https://docs.streamlit.io/)
- [Pydantic](https://docs.pydantic.dev/)
- [Plotly](https://plotly.com/python/)

### Tutoriais Recomendados

- FastAPI Tutorial (oficial) - Completo e didático
- SQLAlchemy ORM - Docs oficiais seção "ORM"
- Streamlit Gallery - Exemplos práticos

---

## 🤔 FAQs

### Por que SQLAlchemy em vez de SQLModel?

SQLAlchemy é maduro (15+ anos), amplamente usado em produção, e tem documentação extensa. SQLModel é mais novo, combina SQLAlchemy + Pydantic de forma elegante, mas ainda está em evolução. Para aprendizado, SQLAlchemy puro ensina os fundamentos.

### Por que não usar async/await?

Para simplificar o protótipo didático. FastAPI suporta async, mas SQLAlchemy tradicional é síncrono. Em produção, considere SQLAlchemy async ou encode/databases.

### Como fazer deploy?

1. Backend: Railway ou Render (suportam Python + banco Postgres)
2. Frontend: Streamlit Cloud (gratuito para projetos públicos)
3. Variáveis de ambiente: Configure DATABASE_URL no host

### Como adicionar autenticação?

1. Instale `python-jose`, `passlib`, `python-multipart`
2. Crie modelo de User
3. Endpoints de login/registro
4. Middleware para validar JWT
5. Relacione items com users (FK)

---

## 📄 Licença

Projeto didático de código aberto - Use livremente! 🎉

---

**Desenvolvido com ❤️ para aprendizado de Python full-stack**
