# 🚀 Finance Tracker - PRONTO PARA USAR!

## ✅ Instalação Completa

Todas as dependências já estão instaladas e o banco de dados foi populado com 20 itens de exemplo!

---

## 🎯 Como Executar (2 Terminais)

### **Terminal 1 - Backend API**

```bash
cd /Users/marceloazevedo/.gemini/antigravity/playground/neon-magnetar/finance-tracker
source venv/bin/activate
cd backend
uvicorn app.main:app --reload
```

✅ **Backend:** http://localhost:8000  
📚 **Swagger (Docs):** http://localhost:8000/docs  
📖 **ReDoc:** http://localhost:8000/redoc

---

### **Terminal 2 - Frontend Streamlit**

```bash
cd /Users/marceloazevedo/.gemini/antigravity/playground/neon-magnetar/finance-tracker
source venv/bin/activate
cd frontend
streamlit run ui/app.py
```

✅ **Interface:** http://localhost:8501 (abre automaticamente no navegador)

---

## 📊 O que você verá

### Backend (FastAPI)
- API REST completa rodando
- Swagger UI interativa
- 20 itens já cadastrados no banco

### Frontend (Streamlit)
- Dashboard com métricas (receitas, despesas, saldo)
- Gráficos por categoria
- Tabela com todos os itens
- Formulário para criar novos itens
- Filtros por tipo, categoria e data

---

## 🧪 Testar a API Direto no Swagger

1. Abra: http://localhost:8000/docs
2. Clique em **GET /api/items** → "Try it out" → "Execute"
3. Você verá os 20 itens de exemplo!

Experimente também:
- **GET /api/balance** - Ver o saldo total
- **GET /api/summary/category** - Totais por categoria
- **POST /api/items** - Criar um novo item

---

## 📋 Dados de Exemplo

O banco já tem:
- **5 receitas** (Salário, Freelance, e tc.)
- **15 despesas** (Alimentação, Transporte, etc.)
- Distribuídos nos **últimos 90 dias**

---

## 🛑 Para Parar

- **Backend**: Ctrl+C no Terminal 1
- **Frontend**: Ctrl+C no Terminal 2

---

## 🔄 Recriar o Banco de Dados

Se quiser limpar e repovoar:

```bash
cd /Users/marceloazevedo/.gemini/antigravity/playground/neon-magnetar/finance-tracker
source venv/bin/activate
rm backend/finance_tracker.db
cd backend
python3 seed_data.py
```

---

## 📁 Estrutura do Projeto

```
finance-tracker/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── main.py      # ⭐ Aplicação principal
│   │   ├── api/routes.py # ⭐ Endpoints
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic validation
│   │   ├── services/    # Business logic
│   │   └── db/          # Database config
│   └── seed_data.py     # ⭐ Dados de exemplo
│
├── frontend/             # Interface Streamlit
│   └── ui/app.py        # ⭐ Interface completa
│
└── venv/                # Ambiente virtual (compartilhado)
```

---

## 🎓 Próximos Passos

1. **Explore a API**: http://localhost:8000/docs
2. **Use o Streamlit**: Criar, filtrar, excluir itens
3. **Estude o código**: Comentado e organizado em camadas
4. **Experimente**: Adicionar novos endpoints, mudar validações

---

## 📚 Documentação

- `README.md` - Documentação completa
- `PROJECT_OVERVIEW.md` - Arquitetura e conceitos
- `QUICKSTART.md` - Guia rápido

---

**Tudo pronto! Bora testar! 🚀**
