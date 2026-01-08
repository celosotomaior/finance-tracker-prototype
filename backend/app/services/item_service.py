"""
Camada de serviço com a lógica de negócio.

Esta camada abstrai as operações de banco de dados e contém
a lógica de negócio da aplicação.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, func, extract
from app.models.item import FinanceItem
from app.schemas.item import FinanceItemCreate, FinanceItemUpdate, ItemType
from typing import List, Optional, Dict, Any
from datetime import date


class ItemService:
    """
    Serviço para gerenciar itens financeiros.
    
    Centraliza toda a lógica de CRUD e cálculos.
    """

    @staticmethod
    def create_item(db: Session, item: FinanceItemCreate) -> FinanceItem:
        """
        Cria um novo item financeiro.
        
        Args:
            db: Sessão do banco de dados
            item: Dados do item a ser criado
            
        Returns:
            FinanceItem criado
        """
        db_item = FinanceItem(
            type=item.type.value,
            category=item.category,
            amount=item.amount,
            date=item.date,
            description=item.description
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def get_item(db: Session, item_id: int) -> Optional[FinanceItem]:
        """
        Busca um item por ID.
        
        Args:
            db: Sessão do banco de dados
            item_id: ID do item
            
        Returns:
            FinanceItem ou None se não encontrado
        """
        return db.query(FinanceItem).filter(FinanceItem.id == item_id).first()

    @staticmethod
    def get_items(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        type_filter: Optional[ItemType] = None,
        category_filter: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[FinanceItem]:
        """
        Lista itens com filtros opcionais.
        
        Args:
            db: Sessão do banco de dados
            skip: Número de itens a pular (paginação)
            limit: Número máximo de itens a retornar
            type_filter: Filtrar por tipo (income/expense)
            category_filter: Filtrar por categoria
            date_from: Data inicial (inclusive)
            date_to: Data final (inclusive)
            
        Returns:
            Lista de FinanceItem
        """
        query = db.query(FinanceItem)
        
        # Aplica filtros se fornecidos
        filters = []
        
        if type_filter:
            filters.append(FinanceItem.type == type_filter.value)
        
        if category_filter:
            # Case-insensitive match
            filters.append(func.lower(FinanceItem.category) == category_filter.lower())
        
        if date_from:
            filters.append(FinanceItem.date >= date_from)
        
        if date_to:
            filters.append(FinanceItem.date <= date_to)
        
        if filters:
            query = query.filter(and_(*filters))
        
        # Ordena por data (mais recente primeiro)
        query = query.order_by(FinanceItem.date.desc())
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_item(
        db: Session,
        item_id: int,
        item_update: FinanceItemUpdate
    ) -> Optional[FinanceItem]:
        """
        Atualiza um item existente.
        
        Args:
            db: Sessão do banco de dados
            item_id: ID do item a atualizar
            item_update: Dados para atualizar (campos opcionais)
            
        Returns:
            FinanceItem atualizado ou None se não encontrado
        """
        db_item = ItemService.get_item(db, item_id)
        
        if not db_item:
            return None
        
        # Atualiza apenas os campos fornecidos
        update_data = item_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            # Converte enum para string se necessário
            if field == "type" and value:
                value = value.value
            setattr(db_item, field, value)
        
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def delete_item(db: Session, item_id: int) -> bool:
        """
        Remove um item.
        
        Args:
            db: Sessão do banco de dados
            item_id: ID do item a remover
            
        Returns:
            True se removido, False se não encontrado
        """
        db_item = ItemService.get_item(db, item_id)
        
        if not db_item:
            return False
        
        db.delete(db_item)
        db.commit()
        return True

    @staticmethod
    def get_summary_by_category(
        db: Session,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Calcula totais por categoria.
        
        Args:
            db: Sessão do banco de dados
            date_from: Data inicial (opcional)
            date_to: Data final (opcional)
            
        Returns:
            Dict com totais por categoria separados por tipo
        """
        query = db.query(
            FinanceItem.type,
            FinanceItem.category,
            func.sum(FinanceItem.amount).label('total')
        )
        
        # Aplica filtros de data
        if date_from:
            query = query.filter(FinanceItem.date >= date_from)
        if date_to:
            query = query.filter(FinanceItem.date <= date_to)
        
        # Agrupa por tipo e categoria
        results = query.group_by(FinanceItem.type, FinanceItem.category).all()
        
        # Organiza os resultados
        summary = {
            "income": {},
            "expense": {}
        }
        
        for type_, category, total in results:
            summary[type_][category] = round(total, 2)
        
        return summary

    @staticmethod
    def get_summary_by_month(
        db: Session,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Calcula totais por mês.
        
        Args:
            db: Sessão do banco de dados
            year: Ano para filtrar (opcional)
            
        Returns:
            Dict com totais mensais separados por tipo
        """
        query = db.query(
            FinanceItem.type,
            extract('year', FinanceItem.date).label('year'),
            extract('month', FinanceItem.date).label('month'),
            func.sum(FinanceItem.amount).label('total')
        )
        
        if year:
            query = query.filter(extract('year', FinanceItem.date) == year)
        
        results = query.group_by(
            FinanceItem.type,
            extract('year', FinanceItem.date),
            extract('month', FinanceItem.date)
        ).order_by('year', 'month').all()
        
        # Organiza os resultados
        summary = []
        
        for type_, year, month, total in results:
            summary.append({
                "type": type_,
                "year": int(year),
                "month": int(month),
                "total": round(total, 2)
            })
        
        return summary

    @staticmethod
    def get_balance(
        db: Session,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> Dict[str, float]:
        """
        Calcula o saldo (receitas - despesas).
        
        Args:
            db: Sessão do banco de dados
            date_from: Data inicial (opcional)
            date_to: Data final (opcional)
            
        Returns:
            Dict com total_income, total_expense e balance
        """
        query = db.query(
            FinanceItem.type,
            func.sum(FinanceItem.amount).label('total')
        )
        
        if date_from:
            query = query.filter(FinanceItem.date >= date_from)
        if date_to:
            query = query.filter(FinanceItem.date <= date_to)
        
        results = query.group_by(FinanceItem.type).all()
        
        totals = {"income": 0.0, "expense": 0.0}
        
        for type_, total in results:
            totals[type_] = round(total, 2)
        
        return {
            "total_income": totals["income"],
            "total_expense": totals["expense"],
            "balance": round(totals["income"] - totals["expense"], 2)
        }
