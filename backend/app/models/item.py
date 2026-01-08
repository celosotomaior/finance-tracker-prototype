"""
Modelo ORM para itens financeiros (despesas e receitas).

Define a estrutura da tabela no banco de dados usando SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class FinanceItem(Base):
    """
    Modelo que representa um item financeiro (despesa ou receita).
    
    Cada item tem tipo (expense/income), categoria, valor, data e descrição.
    """
    __tablename__ = "finance_items"

    # ID auto-incrementado
    id = Column(Integer, primary_key=True, index=True)
    
    # Tipo: 'expense' (despesa) ou 'income' (receita)
    type = Column(String, nullable=False, index=True)
    
    # Categoria: ex: "alimentação", "transporte", "salário"
    category = Column(String, nullable=False, index=True)
    
    # Valor em reais
    amount = Column(Float, nullable=False)
    
    # Data do item financeiro
    date = Column(Date, nullable=False, index=True)
    
    # Descrição opcional
    description = Column(String, nullable=True)
    
    # Timestamps automáticos para auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<FinanceItem(id={self.id}, type={self.type}, amount={self.amount})>"
