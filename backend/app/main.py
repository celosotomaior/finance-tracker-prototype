"""
Ponto de entrada da aplicação FastAPI.

Configura o servidor, CORS, rotas e inicializa o banco de dados.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.db.database import init_db

# Cria a aplicação FastAPI
app = FastAPI(
    title="Finance Tracker API",
    description="API REST para gerenciar despesas e receitas pessoais",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Configuração de CORS para permitir requests do Streamlit
# Em produção, substitua "*" pelos domínios específicos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lista de origens permitidas
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os headers
)

# Inclui as rotas da API
app.include_router(router)


@app.on_event("startup")
def on_startup():
    """
    Executado ao iniciar a aplicação.
    
    Inicializa o banco de dados criando as tabelas necessárias.
    """
    print("🚀 Inicializando banco de dados...")
    init_db()
    print("✅ Banco de dados pronto!")


@app.get("/")
def read_root():
    """
    Endpoint raiz para verificar se a API está funcionando.
    """
    return {
        "message": "Finance Tracker API está rodando! 🚀",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """
    Endpoint de health check para monitoramento.
    """
    return {"status": "healthy", "service": "finance-tracker-api"}
