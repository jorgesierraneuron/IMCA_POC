companies = [
    "General de Alquiler de Maquinaria", # GAM
    "Baeza Machinery Company", # Note: now part of Teselta
    "Teselta",
    "Renta Unida", # Alias for Teselta
    "INMAR RD",
    "CEP Dominicana",
    "CEP Rental", # Alias for CEP Dominicana
    "Agencia Navarro S.R.L.",
    "Busca Maquinaria" # for buscamaquinaria.com related news
]

# --- UPDATED: Comprehensive list of Dominican Republic news sites ---
dominican_sites = [
    "site:listindiario.com",
    "site:diariolibre.com",
    "site:hoy.com.do",
    "site:elnuevodiario.com.do",
    "site:elcaribe.com.do",
    "site:elnacional.com.do",
    "site:lainformacion.com.do",
    "site:eljaya.com",
    "site:almomento.net",
    "site:dominicantoday.com",
    "site:24horas.com.do",
    "site:7dias.com.do",
    "site:acento.com.do",
    "site:ntelemicro.com", # Extracted just the domain
    "site:dominicannews.com",
    "site:dominicanrepublicpost.com",
    "site:dominicanodigital.com",
    "site:.do" # General .do domain for broader searches
]

base_keywords_for_companies = [
    "contrato", "proyecto", "licitación", "inversión", "expansión",
    "nueva maquinaria", "equipo", "adquisición", "sociedad",
    "desarrollo", "infraestructura", "construcción", "alquiler",
    "riesgo", "amenaza", "competencia", "regulatorio" # Added risk-related keywords
]

queries = []

# --- 1. Add your original general queries ---
# Modify these to use the new dominican_sites list for broader coverage
general_search_keywords = [
    "licitaciones públicas infraestructura República Dominicana",
    "proyectos de construcción relevantes República Dominicana",
    "inversiones extranjeras en infraestructura República Dominicana",
    "renovación urbana y zonas industriales República Dominicana",
    "compras públicas de maquinaria empresas constructoras República Dominicana"
]

for keyword_phrase in general_search_keywords:
    for site in dominican_sites:
        queries.append(f'{keyword_phrase} {site} after:2024')

# --- 2. Add specific queries for each company ---
for company in companies:
    # Basic news search for the company on all sites
    for site in dominican_sites:
        queries.append(f'"{company}" {site} after:2024')

    # Search for company + relevant keywords on all sites
    for keyword in base_keywords_for_companies:
        for site in dominican_sites:
            queries.append(f'"{company}" {keyword} {site} after:2024')

# --- 3. Add specific nuanced queries (e.g., mergers, specific events) ---
queries.extend([
    # Queries without specific sites, letting the search engine broaden the net
    "\"Baeza Machinery Company\" Teselta República Dominicana after:2024", # To catch news about their integration
    "Teselta Renta Unida República Dominicana after:2024", # To catch news confirming this alias
    "\"General de Alquiler de Maquinaria\" GAM República Dominicana after:2024", # Specific variant for GAM
    "\"CEP Dominicana\" \"CEP Rental\" República Dominicana after:2024", # To catch news confirming this alias
    "alquiler de maquinaria pesada República Dominicana tendencias after:2024", # Broader market trend
    "sector construcción República Dominicana desafíos after:2024", # Risk-oriented market news
    "financiamiento proyectos infraestructura República Dominicana after:2024", # Financial aspects of infrastructure
    "cambios regulatorios construcción República Dominicana after:2024", # Regulatory risks
    "impacto desastres naturales infraestructura República Dominicana after:2024" # External events risks
])

# Remove potential duplicates by converting to a set and back to a list
queries = list(set(queries))

print(f"Generated {len(queries)} unique search queries.")

print(queries)

# Example of using the queries list:
# You would pass this 'queries' list to your Search utility
# class Search:
#     def run(self, time_range, max_results_per_query_per_site): # Adjusted max_results for more granular control
#         all_results = []
#         # It's crucial how your actual search utility (e.g., Tavily) handles multiple queries
#         # Tavily's .run() usually takes a single query, so you'd loop through these
#         for query_str in queries:
#             # The 'after:2024' is already in the query string, so the time_range param might be redundant
#             # depending on your Tavily integration.
#             results_for_query = self._perform_tavily_search(query_str, max_results_per_query_per_site)
#             all_results.extend(results_for_query)
#         return all_results