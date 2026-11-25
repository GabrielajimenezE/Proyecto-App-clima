import streamlit as st
from src.data import cargar_datos

st.title("🌤️ EcoClima 360")
st.caption("Análisis de Normales Climatológicas Estándar (IDEAM)")

df = cargar_datos()

if not df.empty:
    st.success("✅ ¡Conexión exitosa con el dataset del IDEAM!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Estaciones", f"{len(df):,}")
    with col2:
        total_deps = df["departamento"].nunique() if "departamento" in df.columns else 0
        st.metric("Departamentos", total_deps)
    with col3:
        if "precipitacion_anual_mm" in df.columns:
            prom_precip = df["precipitacion_anual_mm"].mean()
            st.metric("Precipitación Promedio", f"{prom_precip:.1f} mm")

    st.divider()
    st.subheader("📋 Muestra de datos cargados del IDEAM")
    st.dataframe(df.head(20), use_container_width=True)
else:
    st.warning("No se pudieron cargar los datos. Verifica la ruta data/raw/datos.csv")