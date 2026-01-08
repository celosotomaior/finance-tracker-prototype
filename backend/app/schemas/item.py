"""
Schemas Pydantic para validação de dados da API.

Define a estrutura e validação de requests e responses.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import date as date_type, datetime
from typing import Optional, Any
from enum import Enum


class ItemType(str, Enum):
    """Enum para tipos de item: receita ou despesa."""
    INCOME = "income"
    EXPENSE = "expense"


class FinanceItemBase(BaseModel):
    """
    Schema base com campos comuns para criar e exibir itens.
    """
    type: ItemType = Field(..., description="Tipo do item: income ou expense")
    category: str = Field(..., min_length=1, max_length=50, description="Categoria do item")
    amount: float = Field(..., gt=0, description="Valor em reais (deve ser positivo)")
    date: date_type = Field(..., description="Data do item no formato YYYY-MM-DD")
    description: Optional[str] = Field(None, max_length=200, description="Descrição opcional")

    @field_validator('category')
    @classmethod
    def category_must_not_be_empty(cls, v: str) -> str:
        """Valida que categoria não é apenas espaços em branco."""
        if not v.strip():
            raise ValueError('Categoria não pode estar vazia')
        return v.strip()


class FinanceItemCreate(FinanceItemBase):
    """
    Schema para criação de item.
    
    Herda todos os campos de FinanceItemBase.
    """
    pass


class FinanceItemUpdate(BaseModel):
    """
    Schema para atualização de item.
    
    Todos os campos são opcionais para permitir atualização parcial.
    """
    type: Optional[ItemType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[date_type] = None
    description: Optional[str] = Field(None, max_length=200)

    @field_validator('category')
    @classmethod
    def category_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        """Valida que categoria não é apenas espaços em branco."""
        if v is not None and not v.strip():
            raise ValueError('Categoria não pode estar vazia')
        return v.strip() if v else None


class FinanceItemResponse(FinanceItemBase):
    """
    Schema para response da API.
    
    Inclui o ID e timestamps além dos campos base.
    """
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """Configuração do Pydantic para trabalhar com ORM."""
        from_attributes = True  # Permite criar a partir de modelos SQLAlchemy


class StandardResponse(BaseModel):
    """
    Schema para padronizar todas as respostas da API.
    
    Formato: {"data": ..., "error": null} ou {"data": null, "error": "..."}
    """
    data: Optional[Any] = None
    error: Optional[str] = None
