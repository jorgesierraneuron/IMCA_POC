import streamlit as st
import time
from utils.tavily import Search
from utils.llamager import LLamager, CompanyInfo

# Simulando una función que devuelve oportunidades
def fetch_opportunities(company_name, description, time_range, news_count):
    model = "gpt-4.1-mini-2025-04-14"
    company_info = CompanyInfo(company_name, description)
    queries = [
            # 1. Riesgos generales del sector (económicos, de mercado, geopolíticos)
            "\"riesgo sector construcción\" OR \"amenaza infraestructura\" \"República Dominicana\" after:2024",

            # 2. Actividad relevante de competidores clave (expansión, grandes contratos, nuevas tecnologías)
            "\"General de Alquiler de Maquinaria\" OR Teselta OR \"CEP Dominicana\" \"expansión\" OR \"nuevo contrato\" OR \"adquisición\" \"República Dominicana\" after:2024",

            # 3. Cambios regulatorios o legales que afecten el negocio de maquinaria/construcción
            "\"cambios regulatorios\" OR \"nueva ley\" \"maquinaria pesada\" OR \"construcción\" \"República Dominicana\" after:2024",

            # 4. Tendencias del mercado que indiquen desaceleración o inestabilidad económica
            "\"desaceleración económica\" OR \"recesión\" OR \"caída inversión pública\" \"República Dominicana\" after:2024",

            # 5. Amenazas de tecnología o sustitución de servicios/equipos
            "\"tecnología disruptiva\" OR \"sustitución de equipos\" \"alquiler de maquinaria\" OR \"construcción\" \"República Dominicana\" after:2024",

            # --- NUEVA QUERY: Búsqueda general de las empresas clave ---
            "\"General de Alquiler de Maquinaria\" OR GAM OR \"Baeza Machinery Company\" OR Teselta OR \"Renta Unida\" OR \"INMAR RD\" OR \"CEP Dominicana\" OR \"CEP Rental\" OR \"Agencia Navarro S.R.L.\" OR \"Busca Maquinaria\" \"República Dominicana\" after:2024"
        ]

    print(f"name: {company_info.name} description: {company_info.description}")
    search = Search()
    llamager = LLamager(company_info, model, 'riesgo')

    search_query_count = max(1, news_count // 5)
    results = search.run(time_range, search_query_count, queries)
    analyze_news = llamager.analyze(results)
    
    return analyze_news

# --- Configuración y Lógica de la Subpágina ---

st.set_page_config(page_title="Risk Analysis", layout="wide")
st.title("📈 Risk Analysis")

# --- Inicializar variables de estado de sesión ---
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
# NUEVO: Variable para rastrear si se ha intentado una búsqueda
if "search_attempted" not in st.session_state:
    st.session_state.search_attempted = False
# --------------------------------------------------


# Sidebar con filtros
with st.sidebar:
    st.header("🔧 Filtros")
    
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
        st.session_state.company_name = company_name
        st.session_state.description = description
        st.session_state.time_range = time_range
        st.session_state.news_count = news_count
        st.session_state.search_attempted = True # Marcamos que se ha intentado una búsqueda

        with st.spinner("Buscando oportunidades..."):
            st.session_state.results = fetch_opportunities(company_name, description, time_range, news_count)
            st.rerun()

    # Botón de reset para borrar solo los resultados
    if st.button("🧹 Reset Results", key="reset_button_sidebar"):
        st.session_state.results = []
        st.session_state.company_name = ""
        st.session_state.description = ""
        st.session_state.time_range = "day"
        st.session_state.news_count = 5
        st.session_state.search_attempted = False # Resetear el intento de búsqueda también
        st.rerun()

# --- Mostrar los resultados o el mensaje de no encontrados ---
if st.session_state.results:
    st.subheader("🧠 Resultados encontrados")
    
    for item in st.session_state.results:
        with st.container(border=True):
            st.markdown(f"### {item['title']}")
            st.markdown(f"**Source:** [Link]({item['url']})")
            st.markdown(f"**Resume:** {item['content']}")
            st.markdown("---")
            st.markdown("### 📌 Recomendaciones")
            st.markdown(item.get("recomendations", "No recommendations available."), unsafe_allow_html=True)
elif st.session_state.search_attempted: # Solo si se intentó una búsqueda y no hubo resultados
    st.info("⚠️ No se han encontrado riesgos relevantes con los criterios seleccionados. Prueba ajustando el rango de búsqueda o los filtros.")