import os
import sys
import streamlit as st

# Permite importar desde la carpeta src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data import cargar_datos

st.header("👤 Mis Datos y Estadísticas")
st.write("Resumen ejecutivo de los registros cargados en el sistema.")

df = cargar_datos()

if not df.empty:
  st.subheader("📊 Resumen del Dataset")

  col1, col2 = st.columns(2)
  with col1:
    st.metric("Total de Registros", len(df))
    st.metric("Columnas Detectadas", len(df.columns))

  with col2:
    if "departamento" in df.columns:
      st.metric("Departamentos Únicos", df["departamento"].nunique())
    if "municipio" in df.columns:
      st.metric("Municipios Únicos", df["municipio"].nunique())

  st.subheader("Estructura de Columnas")
  st.write(list(df.columns))
else:
  st.warning("No se pudieron cargar los datos. Verifica la carpeta data/raw/.")