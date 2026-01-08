"""
Rotas da API REST.

Define todos os endpoints HTTP e suas validações.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.db.database import get_db
from app.services.item_service import ItemService
from app.schemas.item import (
    FinanceItemCreate,
    FinanceItemUpdate,
    FinanceItemResponse,
    ItemType,
    StandardResponse
)

# Router que será incluído no app principal
router = APIRouter(prefix="/api", tags=["items"])


# ==================== CRUD Endpoints ====================

@router.post("/items", response_model=FinanceItemResponse, status_code=201)
def create_item(
    item: FinanceItemCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo item financeiro.
    
    - **type**: income ou expense
    - **category**: categoria do item
    - **amount**: valor (deve ser positivo)
    - **date**: data no formato YYYY-MM-DD
    - **description**: descrição opcional
    """
    try:
        return ItemService.create_item(db, item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar item: {str(e)}")


@router.get("/items", response_model=List[FinanceItemResponse])
def get_items(
    skip: int = Query(0, ge=0, description="Número de itens a pular"),
    limit: int = Query(100, ge=1, le=500, description="Máximo de itens a retornar"),
    type: Optional[ItemType] = Query(None, description="Filtrar por tipo: income ou expense"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    date_from: Optional[date] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Lista itens com filtros opcionais.
    
    Permite filtrar por tipo, categoria e intervalo de datas.
    Retorna os itens ordenados por data (mais recente primeiro).
    """
    try:
        return ItemService.get_items(
            db,
            skip=skip,
            limit=limit,
            type_filter=type,
            category_filter=category,
            date_from=date_from,
            date_to=date_to
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar itens: {str(e)}")


@router.get("/items/{item_id}", response_model=FinanceItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Busca um item específico por ID.
    """
    item = ItemService.get_item(db, item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} não encontrado")
    
    return item


@router.put("/items/{item_id}", response_model=FinanceItemResponse)
def update_item(
    item_id: int,
    item_update: FinanceItemUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um item existente.
    
    Todos os campos são opcionais - apenas os fornecidos serão atualizados.
    """
    updated_item = ItemService.update_item(db, item_id, item_update)
    
    if not updated_item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} não encontrado")
    
    return updated_item


@router.delete("/items/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove um item.
    
    Retorna 204 No Content se bem-sucedido, 404 se não encontrado.
    """
    deleted = ItemService.delete_item(db, item_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Item {item_id} não encontrado")
    
    return None


# ==================== Análise e Resumos ====================

@router.get("/summary/category")
def get_summary_by_category(
    date_from: Optional[date] = Query(None, description="Data inicial"),
    date_to: Optional[date] = Query(None, description="Data final"),
    db: Session = Depends(get_db)
):
    """
    Retorna totais agrupados por categoria.
    
    Separa income e expense, mostrando quanto foi gasto/recebido por categoria.
    """
    try:
        summary = ItemService.get_summary_by_category(db, date_from, date_to)
        return {"data": summary, "error": None}
    except Exception as e:
        return {"data": None, "error": str(e)}


@router.get("/summary/month")
def get_summary_by_month(
    year: Optional[int] = Query(None, description="Ano para filtrar"),
    db: Session = Depends(get_db)
):
    """
    Retorna totais agrupados por mês.
    
    Útil para gráficos de linha mostrando evolução ao longo do tempo.
    """
    try:
        summary = ItemService.get_summary_by_month(db, year)
        return {"data": summary, "error": None}
    except Exception as e:
        return {"data": None, "error": str(e)}


@router.get("/balance")
def get_balance(
    date_from: Optional[date] = Query(None, description="Data inicial"),
    date_to: Optional[date] = Query(None, description="Data final"),
    db: Session = Depends(get_db)
):
    """
    Retorna o saldo (receitas - despesas).
    
    Mostra total de receitas, total de despesas e o saldo resultante.
    """
    try:
        balance = ItemService.get_balance(db, date_from, date_to)
        return {"data": balance, "error": None}
    except Exception as e:
        return {"data": None, "error": str(e)}
