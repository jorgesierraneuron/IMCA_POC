import streamlit as st
import time
from utils.tavily import Search
from utils.llamager import LLamager, CompanyInfo

# Simulando una función que devuelve oportunidades
def fetch_opportunities(company_name, description, time_range, news_count):
    model = "gpt-4.1-mini-2025-04-14"
    company_info = CompanyInfo(company_name, description)

    queries = [
        "licitaciones públicas infraestructura República Dominicana site:listindiario.com after:2024",
        "proyectos de construcción relevantes República Dominicana site:.do after:2024",
        "inversiones extranjeras en infraestructura República Dominicana site:.do after:2024",
        "renovación urbana y zonas industriales República Dominicana República Dominicana site:.do after:2024", # Corrected typo "República Dominicana República Dominicana"
        "compras públicas de maquinaria empresas constructoras República Dominicana site:.do after:2024"
    ]
    

    print(f"name: {company_info.name} description: {company_info.description}")
    search = Search()
    llamager = LLamager(company_info, model, 'estratega') # 'estratega' indicates opportunity evaluation

    search_query_count = max(1, news_count // 5) 
    results = search.run(time_range, search_query_count, queries) 
    analyze_news = llamager.analyze(results)
    
    return analyze_news

# --- Configuración y Lógica de la Subpágina ---

st.set_page_config(page_title="Opportunity Scanner", layout="wide")
st.title("📈 Opportunity Scanner")

# --- Initialize session state variables ---
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
# NEW: Variable to track if a search has been attempted
if "search_attempted" not in st.session_state:
    st.session_state.search_attempted = False
# --------------------------------------------


# Sidebar with filters
with st.sidebar:
    st.header("🔧 Filters") # Changed to English for consistency with "Opportunity Scanner" title
    
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

    # Button to search for opportunities
    if st.button("🔎 Search Opportunities", key="search_button_sidebar"):
        # Update session state with current filter values
        st.session_state.company_name = company_name
        st.session_state.description = description
        st.session_state.time_range = time_range
        st.session_state.news_count = news_count
        st.session_state.search_attempted = True # Mark that a search was attempted

        with st.spinner("Searching for opportunities..."): # Changed to English
            st.session_state.results = fetch_opportunities(company_name, description, time_range, news_count)
            st.rerun() # This reloads the page to display updated results

    # Reset button to clear only results
    if st.button("🧹 Reset Results", key="reset_button_sidebar"):
        st.session_state.results = []
        # Optional: clear input fields too for a complete reset
        st.session_state.company_name = ""
        st.session_state.description = ""
        st.session_state.time_range = "day"
        st.session_state.news_count = 5
        st.session_state.search_attempted = False # Reset search attempt status
        st.rerun() # Reload to reflect reset

# --- Display results or "no results" message ---
if st.session_state.results:
    st.subheader("🧠 Results Found") # Changed to English
    
    for item in st.session_state.results:
        with st.container(border=True):
            st.markdown(f"### {item['title']}")
            st.markdown(f"**Source:** [Link]({item['url']})")
            st.markdown(f"**Resume:** {item['content']}")
            st.markdown("---")
            st.markdown("### 📌 Recommendations") # Changed to English
            st.markdown(item.get("recomendations", "No recommendations available."), unsafe_allow_html=True)
elif st.session_state.search_attempted: # Only if a search was attempted AND no results were found
    st.info("⚠️ No se han encontrado oportunidades con los criterios seleccionados. Prueba ajustando el rango de búsqueda o los filtros.") # Changed to English