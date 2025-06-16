import streamlit as st
import time # Aunque no se usa directamente en este snippet, lo dejo por si lo necesitas
from utils.tavily import Search
from utils.llamager import LLamager, CompanyInfo

# Simulando una función que devuelve oportunidades
def fetch_opportunities(company_name, description, time_range, news_count):
    model = "gpt-4.1-mini-2025-04-14"
    company_info = CompanyInfo(company_name, description)

    print(f"name: {company_info.name} description: {company_info.description}")
    search = Search()
    llamager = LLamager(company_info, model, 'estratega')

    # Ajuste de la cantidad de noticias, asegurando que news_count // 5 no sea cero para evitar errores
    # Asegúrate que Search.run pueda manejar un news_count de 0 si news_count es 0
    search_query_count = max(1, news_count // 5) 
    results = search.run(time_range, search_query_count) 
    analyze_news = llamager.analyze(results)
    
    return analyze_news

# --- Configuración y Lógica de la Subpágina ---

# Configuración de la página (solo para esta subpágina)
st.set_page_config(page_title="Opportunity Scanner", layout="wide") # page_title será el título de la pestaña del navegador
st.title("📈 Opportunity Scanner") # Este será el título visible en la página

# Inicializar el estado de sesión si no existe
if "results" not in st.session_state:
    st.session_state.results = []
if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "description" not in st.session_state:
    st.session_state.description = ""
if "time_range" not in st.session_state:
    st.session_state.time_range = "day"
if "news_count" not in st.session_state:
    st.session_state.news_count = 5


# Sidebar con filtros
with st.sidebar:
    st.header("🔧 Filtros")
    
    # Usar st.session_state para mantener los valores en los widgets después de una ejecución
    company_name = st.text_input("Company Name", value=st.session_state.company_name)
    description = st.text_area("Description", value=st.session_state.description)
    time_range = st.selectbox(
        "Time Range", 
        ["day", "week", "month", "year"], 
        index=["day", "week", "month", "year"].index(st.session_state.time_range)
    )
    news_count = st.selectbox(
        "News to Analyze", 
        [5, 10, 15, 20, 25], 
        index=[5, 10, 15, 20, 25].index(st.session_state.news_count)
    )

    # Botón para buscar oportunidades
    if st.button("🔎 Search Opportunities", key="search_button_sidebar"):
        # Actualizar el estado de sesión con los nuevos valores de los filtros
        st.session_state.company_name = company_name
        st.session_state.description = description
        st.session_state.time_range = time_range
        st.session_state.news_count = news_count

        with st.spinner("Buscando oportunidades..."):
            st.session_state.results = fetch_opportunities(company_name, description, time_range, news_count)
            st.rerun() # Esto recarga la página para mostrar los resultados actualizados

    # Botón de reset para borrar solo los resultados
    if st.button("🧹 Reset Results", key="reset_button_sidebar"):
        st.session_state.results = []
        # Opcional: limpiar también los campos de entrada si quieres un reseteo completo
        st.session_state.company_name = ""
        st.session_state.description = ""
        st.session_state.time_range = "day"
        st.session_state.news_count = 5
        st.rerun() # Recarga para reflejar el reseteo

# Mostrar los resultados si existen
if st.session_state.results:
    st.subheader("🧠 Resultados encontrados")
    
    for item in st.session_state.results:
        with st.container(border=True): # Añadido un borde para mejor separación visual
            st.markdown(f"### {item['title']}")
            st.markdown(f"**Source:** [Link]({item['url']})")
            st.markdown(f"**Resume:** {item['content']}")
            st.markdown("---")
            st.markdown("### 📌 Recomendaciones")
            st.markdown(item.get("recomendations", "No recommendations available."), unsafe_allow_html=True)
            # st.markdown("---") # Si usas border=True en el container, este "---" podría ser redundante