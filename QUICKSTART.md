# 🚀 Guia Rápido de Início

## Iniciar o Projeto em 3 Passos

### 1️⃣ Backend (Terminal 1)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py  # Opcional: dados de exemplo
uvicorn app.main:app --reload
```

✅ Backend rodando em: http://localhost:8000  
📚 Documentação da API: http://localhost:8000/docs

---

### 2️⃣ Frontend (Terminal 2)

```bash
cd frontend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run ui/app.py
```

✅ Interface web em: http://localhost:8501

---

### 3️⃣ Testar

1. Abra http://localhost:8501
2. Crie uma receita ou despesa
3. Veja os gráficos e totais atualizados
4. Explore a documentação da API em http://localhost:8000/docs

---

## 💡 Dicas

- Use `seed_data.py` para ter 20 itens de exemplo prontos
- A URL da API pode ser configurada na sidebar do Streamlit
- Todos os endpoints estão documentados automaticamente no Swagger

## 🔧 Comandos Úteis

```bash
# Parar o backend: Ctrl+C
# Parar o frontend: Ctrl+C

# Limpar o banco de dados
rm backend/finance_tracker.db
python backend/seed_data.py

# Atualizar dependências
pip install --upgrade -r requirements.txt
```

---

**Boa codificação! 🎉**
