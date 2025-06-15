import streamlit as st
import time
from utils.tavily import Search
from utils.llamager import LLamager, CompanyInfo

# Simulando una función que devuelve oportunidades
def fetch_opportunities(company_name, description, time_range, news_count):
    model = "gpt-4.1-mini-2025-04-14"
    company_info = CompanyInfo(company_name, description)

    print(f"name: {company_info.name} description: {company_info.description}")
    search = Search()
    llamager = LLamager(company_info, model)

    results = search.run(time_range, news_count // 5)  # Ajuste de la cantidad de noticias
    analyze_news = llamager.analyze(results)
    
    return analyze_news

# Configuración general
st.set_page_config(page_title="Opportunity Scanner", layout="wide")
st.title("📈 Opportunity Scanner")

# Inicializar el estado de sesión si no existe
if "results" not in st.session_state:
    st.session_state.results = []

# Sidebar con filtros
with st.sidebar:
    st.header("🔧 Filtros")
    company_name = st.text_input("Company Name", value=st.session_state.get("company_name", ""))
    description = st.text_area("Description", value=st.session_state.get("description", ""))
    time_range = st.selectbox("Time Range", ["day", "week", "month", "year"], index=["day", "week", "month", "year"].index(st.session_state.get("time_range", "day")))
    news_count = st.selectbox("News to Analyze", [5, 10, 15, 20, 25], index=[5, 10, 15, 20, 25].index(st.session_state.get("news_count", 5)))

    # Botón para buscar oportunidades
    if st.button("🔎 Search Opportunities", key="search_button_sidebar"):
        st.session_state.company_name = company_name
        st.session_state.description = description
        st.session_state.time_range = time_range
        st.session_state.news_count = news_count

        with st.spinner("Buscando oportunidades..."):
            st.session_state.results = fetch_opportunities(company_name, description, time_range, news_count)

    # Botón de reset para borrar solo los resultados
    if st.button("🧹 Reset Results", key="reset_button_sidebar"):
        st.session_state.results = []

# Mostrar los resultados si existen
if st.session_state.results:
    st.subheader("🧠 Resultados encontrados")
    
    for item in st.session_state.results:
        with st.container():
            st.markdown(f"### {item['title']}")
            st.markdown(f"**Source:** [Link]({item['url']})")
            st.markdown(f"**Resume:** {item['content']}")
            st.markdown("---")
            st.markdown("### 📌 Recomendaciones")
            st.markdown(item["recomendations"], unsafe_allow_html=True)
            st.markdown("---")

