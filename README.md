# Finance Tracker 💰

Um protótipo didático para aprender desenvolvimento backend com **FastAPI** e frontend com **Streamlit**, tudo em Python.

## 📋 Sobre o Projeto

Este é um aplicativo completo de controle financeiro pessoal com:

- ✅ Cadastro de despesas e receitas
- ✅ Listagem com filtros (tipo, categoria, data)
- ✅ Cálculos de totais e saldo
- ✅ Gráficos interativos por categoria
- ✅ Edição e remoção de itens
- ✅ Arquitetura organizada em camadas

## 🏗️ Arquitetura

### Backend (FastAPI)

```
backend/
├── app/
│   ├── main.py           # Ponto de entrada da API
│   ├── api/
│   │   └── routes.py     # Endpoints REST
│   ├── models/
│   │   └── item.py       # Modelos SQLAlchemy
│   ├── schemas/
│   │   └── item.py       # Schemas Pydantic
│   ├── services/
│   │   └── item_service.py  # Lógica de negócio
│   └── db/
│       └── database.py   # Configuração do banco
├── requirements.txt
├── .env.example
└── seed_data.py          # Dados de exemplo
```

**Tecnologias:**
- FastAPI para API REST
- SQLAlchemy para ORM
- Pydantic para validação
- SQLite para persistência
- CORS habilitado

### Frontend (Streamlit)

```
frontend/
├── ui/
│   └── app.py           # Interface completa
└── requirements.txt
```

**Tecnologias:**
- Streamlit para UI
- Plotly para gráficos
- Pandas para manipulação de dados
- Requests para consumir API

## 🚀 Como Executar

### Pré-requisitos

- Python 3.9+ instalado
- pip ou venv para gerenciar dependências

### Passo 1: Configurar o Backend

```bash
# Entre na pasta do backend
cd backend

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# (Opcional) Configure variáveis de ambiente
cp .env.example .env

# (Opcional) Popule o banco com dados de exemplo
python seed_data.py

# Inicie o servidor FastAPI
uvicorn app.main:app --reload
```

O backend estará rodando em: **http://localhost:8000**

- Documentação Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Passo 2: Configurar o Frontend

Em outro terminal:

```bash
# Entre na pasta do frontend
cd frontend

# Crie um ambiente virtual (pode usar o mesmo do backend se preferir)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Inicie o Streamlit
streamlit run ui/app.py
```

O frontend abrirá automaticamente em: **http://localhost:8501**

## 📚 Endpoints da API

### Itens Financeiros

- `POST /api/items` - Criar item
- `GET /api/items` - Listar itens (com filtros)
- `GET /api/items/{id}` - Buscar item por ID
- `PUT /api/items/{id}` - Atualizar item
- `DELETE /api/items/{id}` - Remover item

### Análises

- `GET /api/summary/category` - Totais por categoria
- `GET /api/summary/month` - Totais por mês
- `GET /api/balance` - Saldo (receitas - despesas)

### Filtros Disponíveis

- `type`: income ou expense
- `category`: nome da categoria
- `date_from`: data inicial (YYYY-MM-DD)
- `date_to`: data final (YYYY-MM-DD)

## 🧪 Testando a API

### Com cURL

```bash
# Criar uma receita
curl -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{
    "type": "income",
    "category": "Salário",
    "amount": 5000.00,
    "date": "2026-01-07",
    "description": "Salário janeiro"
  }'

# Listar todos os itens
curl http://localhost:8000/api/items

# Buscar saldo
curl http://localhost:8000/api/balance
```

### Com Python

```python
import requests

# Criar uma despesa
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

## 🎨 Recursos do Frontend

1. **Dashboard Principal**
   - Métricas de receitas, despesas e saldo
   - Filtros por tipo, categoria e período

2. **Formulário de Cadastro**
   - Validação automática
   - Feedback de sucesso/erro

3. **Tabela de Itens**
   - Listagem com todos os dados
   - Opção de exclusão por ID

4. **Gráficos**
   - Barras: Despesas por categoria
   - Pizza: Distribuição de receitas

5. **Configurações**
   - URL da API configurável
   - Filtros persistentes na sidebar

## 🛠️ Personalização

### Adicionar Nova Categoria

Basta criar um item com a categoria desejada - o sistema aceita qualquer texto.

### Modificar Validações

Edite os schemas em `backend/app/schemas/item.py`:

```python
amount: float = Field(..., gt=0, lt=1000000)  # Limite máximo
category: str = Field(..., min_length=1, max_length=50)
```

### Adicionar Novo Endpoint

1. Adicione lógica em `services/item_service.py`
2. Crie o endpoint em `api/routes.py`
3. (Opcional) Atualize o frontend em `ui/app.py`

## 📖 Conceitos Didáticos

### Trade-offs de Design

**SQLAlchemy vs SQLModel:**
- Escolhi **SQLAlchemy** puro por ser mais estabelecido e ter mais recursos de documentação
- SQLModel seria uma alternativa moderna que combina SQLAlchemy + Pydantic, mas ainda em evolução

**Estrutura em Camadas:**
- **Models:** Representação do banco de dados
- **Schemas:** Validação e serialização (API)
- **Services:** Lógica de negócio isolada
- **Routes:** Apenas HTTP handlers

**Benefícios:**
- Separação de responsabilidades
- Facilita testes unitários
- Código reutilizável

### Banco de Dados

SQLite foi escolhido por:
- ✅ Zero configuração
- ✅ Ideal para prototipagem
- ✅ Arquivo único portável
- ⚠️ **Produção:** Migrar para PostgreSQL/MySQL

### CORS

Habilitado para permitir que Streamlit consuma a API:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: especifique domínios
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔍 Troubleshooting

### Backend não inicia

```bash
# Verifique se a porta 8000 está livre
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Mude a porta se necessário
uvicorn app.main:app --reload --port 8001
```

### Frontend não conecta à API

1. Verifique se o backend está rodando
2. No Streamlit, abra "Configurações" na sidebar
3. Confirme que a URL é `http://localhost:8000/api`

### Erro de importação

```bash
# Certifique-se de estar na pasta correta
cd backend  # ou frontend
pip install -r requirements.txt
```

## 📝 Próximos Passos (Sugestões)

- [ ] Adicionar autenticação (JWT)
- [ ] Implementar testes unitários
- [ ] Criar migrations com Alembic
- [ ] Adicionar paginação nos endpoints
- [ ] Export/import para CSV/Excel
- [ ] Deploy (Railway, Heroku, Streamlit Cloud)
- [ ] Gráfico de linha para evolução mensal
- [ ] Categorias predefinidas (seed)
- [ ] Múltiplas contas bancárias

## 📄 Licença

Este é um projeto didático de código aberto. Use e modifique à vontade! 🚀

## 🤝 Contribuições

Este projeto foi criado para fins educacionais. Sinta-se livre para:
- Fazer fork
- Abrir issues
- Sugerir melhorias
- Compartilhar com outros estudantes

---

**Desenvolvido com ❤️ usando FastAPI + Streamlit**
