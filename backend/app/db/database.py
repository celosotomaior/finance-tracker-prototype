"""
Configuração do banco de dados SQLite com SQLAlchemy.

Este módulo estabelece a conexão com SQLite e fornece a sessão
para interagir com o banco de dados.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL do banco de dados SQLite
# Usa uma variável de ambiente ou padrão para arquivo local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./finance_tracker.db")

# Engine do SQLAlchemy
# check_same_thread=False é necessário para SQLite com FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal: factory para criar sessões de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: classe base para nossos modelos ORM
Base = declarative_base()


def get_db():
    """
    Dependency Injection para FastAPI.
    
    Cria uma nova sessão de banco de dados para cada request
    e garante que ela será fechada após o uso.
    
    Yields:
        Session: Sessão do SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas.
    
    Deve ser chamado uma vez ao iniciar a aplicação.
    """
    # Importa todos os modelos para que Base.metadata os conheça
    from app.models import item  # noqa: F401
    
    Base.metadata.create_all(bind=engine)
