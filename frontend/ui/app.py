"""
Interface Streamlit para o Finance Tracker.

Consome a API FastAPI para gerenciar despesas e receitas.
"""

import streamlit as st
import requests
import pandas as pd
from datetime import date, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Dict, Any

# Configuração da página
st.set_page_config(
    page_title="Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== Configuração da API ====================

# URL base da API (prioriza secrets no Streamlit Cloud, depois localhost)
if "api_url" not in st.session_state:
    # Tenta ler das secrets do Streamlit Cloud (produção)
    try:
        st.session_state.api_url = st.secrets.get("API_URL", "http://localhost:8000/api")
    except (AttributeError, FileNotFoundError):
        # Fallback para localhost (desenvolvimento local)
        st.session_state.api_url = "http://localhost:8000/api"


def get_api_url() -> str:
    """Retorna a URL base da API."""
    return st.session_state.api_url


# ==================== Funções de API ====================

def call_api(method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Optional[Any]:
    """
    Chama a API e retorna o resultado.
    
    Args:
        method: Método HTTP (GET, POST, PUT, DELETE)
        endpoint: Endpoint da API (ex: '/items')
        data: Dados para POST/PUT
        params: Query params para GET
        
    Returns:
        Response JSON ou None em caso de erro
    """
    url = f"{get_api_url()}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        else:
            st.error(f"Método HTTP inválido: {method}")
            return None
        
        response.raise_for_status()
        
        # DELETE retorna 204 sem conteúdo
        if response.status_code == 204:
            return {"success": True}
        
        return response.json()
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Erro: Não foi possível conectar à API. Verifique se o backend está rodando.")
        return None
    except requests.exceptions.Timeout:
        st.error("❌ Erro: Timeout na conexão com a API.")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Erro HTTP: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        st.error(f"❌ Erro inesperado: {str(e)}")
        return None


# ==================== Funções de Negócio ====================

def create_item(type_: str, category: str, amount: float, item_date: date, description: str) -> bool:
    """Cria um novo item."""
    data = {
        "type": type_,
        "category": category,
        "amount": amount,
        "date": item_date.isoformat(),
        "description": description
    }
    
    result = call_api("POST", "/items", data=data)
    return result is not None


def get_items(type_filter: Optional[str] = None, category_filter: Optional[str] = None, 
              date_from: Optional[date] = None, date_to: Optional[date] = None) -> Optional[pd.DataFrame]:
    """Busca itens com filtros."""
    params = {}
    
    if type_filter:
        params["type"] = type_filter
    if category_filter:
        params["category"] = category_filter
    if date_from:
        params["date_from"] = date_from.isoformat()
    if date_to:
        params["date_to"] = date_to.isoformat()
    
    result = call_api("GET", "/items", params=params)
    
    if result and isinstance(result, list):
        if len(result) == 0:
            return pd.DataFrame()
        return pd.DataFrame(result)
    
    return None


def update_item(item_id: int, **kwargs) -> bool:
    """Atualiza um item existente."""
    # Remove valores None
    data = {k: v for k, v in kwargs.items() if v is not None}
    
    # Converte date para string
    if "date" in data and isinstance(data["date"], date):
        data["date"] = data["date"].isoformat()
    
    result = call_api("PUT", f"/items/{item_id}", data=data)
    return result is not None


def delete_item(item_id: int) -> bool:
    """Deleta um item."""
    result = call_api("DELETE", f"/items/{item_id}")
    return result is not None


def get_balance(date_from: Optional[date] = None, date_to: Optional[date] = None) -> Optional[Dict]:
    """Busca o saldo."""
    params = {}
    if date_from:
        params["date_from"] = date_from.isoformat()
    if date_to:
        params["date_to"] = date_to.isoformat()
    
    result = call_api("GET", "/balance", params=params)
    
    if result and "data" in result:
        return result["data"]
    
    return None


def get_summary_by_category(date_from: Optional[date] = None, date_to: Optional[date] = None) -> Optional[Dict]:
    """Busca resumo por categoria."""
    params = {}
    if date_from:
        params["date_from"] = date_from.isoformat()
    if date_to:
        params["date_to"] = date_to.isoformat()
    
    result = call_api("GET", "/summary/category", params=params)
    
    if result and "data" in result:
        return result["data"]
    
    return None


# ==================== UI Components ====================

def render_sidebar():
    """Renderiza a sidebar com configurações e filtros."""
    with st.sidebar:
        st.title("💰 Finance Tracker")
        
        # Configuração da API
        with st.expander("⚙️ Configurações"):
            api_url = st.text_input(
                "URL da API",
                value=st.session_state.api_url,
                help="URL base da API FastAPI"
            )
            if api_url != st.session_state.api_url:
                st.session_state.api_url = api_url
                st.rerun()
        
        st.divider()
        
        # Filtros
        st.subheader("🔍 Filtros")
        
        # Filtro de tipo
        type_options = ["Todos", "Receitas", "Despesas"]
        type_choice = st.selectbox("Tipo", type_options, key="filter_type")
        
        type_filter = None
        if type_choice == "Receitas":
            type_filter = "income"
        elif type_choice == "Despesas":
            type_filter = "expense"
        
        # Filtro de categoria
        category_filter = st.text_input("Categoria", key="filter_category", placeholder="Ex: Alimentação")
        category_filter = category_filter.strip() if category_filter else None
        
        # Filtro de datas
        st.write("**Período**")
        col1, col2 = st.columns(2)
        
        with col1:
            date_from = st.date_input(
                "De",
                value=date.today() - timedelta(days=30),
                key="filter_date_from"
            )
        
        with col2:
            date_to = st.date_input(
                "Até",
                value=date.today(),
                key="filter_date_to"
            )
        
        return {
            "type": type_filter,
            "category": category_filter,
            "date_from": date_from,
            "date_to": date_to
        }


def render_metrics(filters: Dict):
    """Renderiza as métricas de saldo."""
    st.subheader("📊 Resumo Financeiro")
    
    balance_data = get_balance(filters["date_from"], filters["date_to"])
    
    if balance_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "💸 Total Receitas",
                f"R$ {balance_data['total_income']:,.2f}",
                delta=None,
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                "💳 Total Despesas",
                f"R$ {balance_data['total_expense']:,.2f}",
                delta=None,
                delta_color="inverse"
            )
        
        with col3:
            balance = balance_data['balance']
            st.metric(
                "💰 Saldo",
                f"R$ {balance:,.2f}",
                delta=None,
                delta_color="normal" if balance >= 0 else "inverse"
            )
    else:
        st.info("📊 Nenhum dado disponível para o período selecionado.")


def render_charts(filters: Dict):
    """Renderiza os gráficos de análise."""
    summary_data = get_summary_by_category(filters["date_from"], filters["date_to"])
    
    if not summary_data:
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Despesas por Categoria")
        
        expenses = summary_data.get("expense", {})
        
        if expenses:
            df_expenses = pd.DataFrame([
                {"Categoria": k, "Valor": v}
                for k, v in expenses.items()
            ])
            
            fig = px.bar(
                df_expenses,
                x="Categoria",
                y="Valor",
                color="Categoria",
                title="Despesas por Categoria"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma despesa no período.")
    
    with col2:
        st.subheader("💵 Receitas por Categoria")
        
        incomes = summary_data.get("income", {})
        
        if incomes:
            df_incomes = pd.DataFrame([
                {"Categoria": k, "Valor": v}
                for k, v in incomes.items()
            ])
            
            fig = px.pie(
                df_incomes,
                values="Valor",
                names="Categoria",
                title="Distribuição de Receitas"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma receita no período.")


def render_item_form():
    """Renderiza o formulário para criar/editar itens."""
    st.subheader("➕ Novo Item")
    
    with st.form("item_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            type_ = st.selectbox(
                "Tipo *",
                ["income", "expense"],
                format_func=lambda x: "Receita" if x == "income" else "Despesa"
            )
        
        with col2:
            category = st.text_input("Categoria *", placeholder="Ex: Alimentação")
        
        col3, col4 = st.columns(2)
        
        with col3:
            amount = st.number_input("Valor (R$) *", min_value=0.01, step=0.01, format="%.2f")
        
        with col4:
            item_date = st.date_input("Data *", value=date.today())
        
        description = st.text_area("Descrição", placeholder="Informações adicionais (opcional)")
        
        submitted = st.form_submit_button("💾 Salvar Item", use_container_width=True)
        
        if submitted:
            if not category.strip():
                st.error("⚠️ Categoria é obrigatória!")
            elif amount <= 0:
                st.error("⚠️ Valor deve ser maior que zero!")
            else:
                with st.spinner("Salvando..."):
                    success = create_item(type_, category.strip(), amount, item_date, description.strip())
                
                if success:
                    st.success("✅ Item criado com sucesso!")
                    st.rerun()


def render_items_table(filters: Dict):
    """Renderiza a tabela de itens com opções de edição/exclusão."""
    st.subheader("📋 Lista de Itens")
    
    df = get_items(
        type_filter=filters["type"],
        category_filter=filters["category"],
        date_from=filters["date_from"],
        date_to=filters["date_to"]
    )
    
    if df is None:
        return
    
    if df.empty:
        st.info("📭 Nenhum item encontrado com os filtros selecionados.")
        return
    
    # Formata o DataFrame
    df["type"] = df["type"].map({"income": "Receita", "expense": "Despesa"})
    df["amount"] = df["amount"].apply(lambda x: f"R$ {x:,.2f}")
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d/%m/%Y")
    
    # Renomeia colunas
    df_display = df[["id", "type", "category", "amount", "date", "description"]].copy()
    df_display.columns = ["ID", "Tipo", "Categoria", "Valor", "Data", "Descrição"]
    
    # Exibe a tabela
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Opções de edição/exclusão
    st.divider()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        item_id = st.number_input(
            "ID do item para editar/excluir",
            min_value=1,
            step=1,
            key="item_id_action"
        )
    
    with col2:
        st.write("")  # Espaçamento
        st.write("")  # Espaçamento
        
        if st.button("🗑️ Excluir", use_container_width=True):
            with st.spinner("Excluindo..."):
                success = delete_item(item_id)
            
            if success:
                st.success("✅ Item excluído com sucesso!")
                st.rerun()


# ==================== Main App ====================

def main():
    """Função principal da aplicação."""
    
    # Renderiza a sidebar e obtém os filtros
    filters = render_sidebar()
    
    # Container principal
    st.title("💰 Finance Tracker")
    st.markdown("Gerencie suas finanças pessoais de forma simples e eficiente.")
    
    st.divider()
    
    # Métricas
    render_metrics(filters)
    
    st.divider()
    
    # Gráficos
    render_charts(filters)
    
    st.divider()
    
    # Formulário e tabela
    col1, col2 = st.columns([1, 2])
    
    with col1:
        render_item_form()
    
    with col2:
        render_items_table(filters)
    
    # Rodapé
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <small>Finance Tracker v1.0 | Desenvolvido com FastAPI + Streamlit</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
