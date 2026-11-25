import streamlit as st

st.set_page_config(
    page_title="EcoClima 360",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.image("assets/logo.png")

pag = st.navigation(
    [
        st.Page("pages/01_inicio.py", title="Inicio", icon="🏠"),
        st.Page("pages/03_explorar.py", title="Explorar", icon="🔍"),
        st.Page("pages/04_jugar.py", title="Jugar", icon="🎮"),
        st.Page("pages/05_mis_datos.py", title="Mis Datos", icon="📊"),
    ]
)

pag.run()

st.divider()
st.caption("© 2026 EcoClima 360. Equipo Ingeniería Industrial UdeA. Creative Commons BY-NC 4.0")