from pathlib import Path
import pandas as pd
import streamlit as st


@st.cache_data
def cargar_datos():
    """Carga los datos del IDEAM desde data/raw/datos.csv usando rutas dinámicas."""
    ruta_base = Path(__file__).resolve().parent.parent
    ruta_csv = ruta_base / "data" / "raw" / "datos.csv"

    if not ruta_csv.exists():
        st.error(f"❌ El archivo no existe en la ruta: `{ruta_csv}`")
        return pd.DataFrame()

    try:
        df = pd.read_csv(ruta_csv)
        return df
    except Exception as e:
        st.error(f"❌ Error al leer el CSV: {e}")
        return pd.DataFrame()


def filtrar_datos(df, estacion=None, departamento=None, municipio=None, precip_min=None):
    """Aplica filtros acumulativos por texto y rango numérico sobre el DataFrame."""
    df_res = df.copy()

    if departamento and departamento != "Todos" and "departamento" in df_res.columns:
        df_res = df_res[df_res["departamento"] == departamento]

    if municipio and "municipio" in df_res.columns:
        df_res = df_res[
            df_res["municipio"].astype(str).str.contains(
                municipio.strip(), case=False, regex=False, na=False
            )
        ]

    if estacion:
        col_est = next((c for c in ["estacion", "nombre_estacion", "Estacion"] if c in df_res.columns), None)
        if col_est:
            df_res = df_res[
                df_res[col_est].astype(str).str.contains(
                    estacion.strip(), case=False, regex=False, na=False
                )
            ]

    if precip_min is not None and "precipitacion_anual_mm" in df_res.columns:
        df_res = df_res[df_res["precipitacion_anual_mm"] >= precip_min]

    return df_res