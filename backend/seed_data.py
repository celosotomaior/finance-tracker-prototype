"""
Script para popular o banco de dados com dados de exemplo.

Execute: python seed_data.py
"""

from datetime import date, timedelta
from app.db.database import SessionLocal, init_db
from app.models.item import FinanceItem
import random

# Dados de exemplo
CATEGORIES_INCOME = ["Salário", "Freelance", "Investimentos", "Outros"]
CATEGORIES_EXPENSE = ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Educação"]

DESCRIPTIONS = {
    "Salário": ["Salário mensal", "Adiantamento", "13º salário"],
    "Freelance": ["Projeto X", "Consultoria", "Design"],
    "Investimentos": ["Dividendos", "Rendimento CDB", "Lucro ações"],
    "Outros": ["Bônus", "Presente", "Reembolso"],
    "Alimentação": ["Supermercado", "Restaurante", "Delivery", "Padaria"],
    "Transporte": ["Uber", "Gasolina", "Estacionamento", "Manutenção"],
    "Moradia": ["Aluguel", "Condomínio", "Luz", "Água", "Internet"],
    "Lazer": ["Cinema", "Streaming", "Viagem", "Passeio"],
    "Saúde": ["Farmácia", "Consulta", "Academia"],
    "Educação": ["Curso online", "Livros", "Material"]
}


def create_sample_items():
    """Cria 20 itens de exemplo nos últimos 3 meses."""
    
    # Inicializa o banco
    init_db()
    db = SessionLocal()
    
    try:
        # Limpa dados existentes (cuidado em produção!)
        db.query(FinanceItem).delete()
        db.commit()
        
        today = date.today()
        items_created = 0
        
        # Cria receitas (5 itens)
        for i in range(5):
            category = random.choice(CATEGORIES_INCOME)
            days_ago = random.randint(0, 90)
            item_date = today - timedelta(days=days_ago)
            
            # Valores maiores para receitas
            amount = round(random.uniform(1000, 5000), 2)
            
            item = FinanceItem(
                type="income",
                category=category,
                amount=amount,
                date=item_date,
                description=random.choice(DESCRIPTIONS[category])
            )
            db.add(item)
            items_created += 1
        
        # Cria despesas (15 itens)
        for i in range(15):
            category = random.choice(CATEGORIES_EXPENSE)
            days_ago = random.randint(0, 90)
            item_date = today - timedelta(days=days_ago)
            
            # Valores menores para despesas
            amount = round(random.uniform(20, 800), 2)
            
            item = FinanceItem(
                type="expense",
                category=category,
                amount=amount,
                date=item_date,
                description=random.choice(DESCRIPTIONS[category])
            )
            db.add(item)
            items_created += 1
        
        db.commit()
        print(f"✅ {items_created} itens de exemplo criados com sucesso!")
        
        # Mostra resumo
        total_income = db.query(FinanceItem).filter(FinanceItem.type == "income").count()
        total_expense = db.query(FinanceItem).filter(FinanceItem.type == "expense").count()
        
        print(f"   - Receitas: {total_income}")
        print(f"   - Despesas: {total_expense}")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Criando dados de exemplo...")
    create_sample_items()
