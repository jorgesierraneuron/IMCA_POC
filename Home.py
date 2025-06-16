import streamlit as st

st.set_page_config(page_title="Mi App Principal", layout="centered")
st.title("IMCA: Data Scanner")

# --- Add your image here ---
# Option 1: From a local file
# Make sure 'your_image.png' is in the same directory as your Home.py file,
# or provide the correct relative path (e.g., 'images/your_image.png')
st.image("logo-imca-dominicana.png", caption="", use_container_width=True)

# Option 2: From a URL (e.g., from an online source)
# st.image("https://example.com/your_online_image.jpg", caption="Imagen desde la web", use_column_width=True)
# ---------------------------

st.write("""
POC para la busqueda de noticias relevantes y extracciòn de oportunidades
""")



# Puedes añadir más contenido aquí, como gráficos de resumen, explicaciones, etc.