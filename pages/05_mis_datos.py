import pandas as pd
import plotly.express as px
import streamlit as st
from src.data import cargar_datos

df = cargar_datos()

st.title("🗂️ Mis Datos y Estadísticas")
st.write(
    "Consulta el estado del conjunto de datos meteorológicos del **IDEAM** y revisa "
    "tu historial de desempeño en el **Desafío Climático**."
)

if df.empty:
    st.warning("No se encontró el archivo de datos en `data/raw/datos.csv`.")
    st.stop()

# 1. RESUMEN EJECUTIVO DEL DATASET IDEAM
st.subheader("📊 Auditoría del Conjunto de Datos (IDEAM)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Estaciones registradas", f"{len(df):,}")
col2.metric("Variables disponibles", len(df.columns))
col3.metric("Departamentos", df["departamento"].nunique() if "departamento" in df.columns else "N/D")
col4.metric("Municipios", df["municipio"].nunique() if "municipio" in df.columns else "N/D")

with st.expander("📋 Ver detalle técnico de las variables del dataset", expanded=False):
    info_columnas = pd.DataFrame(
        {
            "Variable": df.columns,
            "Tipo de dato": df.dtypes.astype(str).values,
            "Registros válidos": df.notnull().sum().values,
        }
    )
    st.dataframe(info_columnas, use_container_width=True, hide_index=True)

st.divider()

# 2. HISTORIAL Y ESTADÍSTICAS DE JUEGO DEL USUARIO
st.subheader("🎮 Historial y Estadísticas del Desafío Climático")

historial = st.session_state.get("historial_juegos", [])
intentos_en_curso = st.session_state.get("intentos", 0)
puntaje_en_curso = st.session_state.get("puntaje", 0)
partida_guardada = st.session_state.get("partida_guardada", False)

# Calcular acumulados (partidas finalizadas + progreso activo si hay una ronda sin terminar)
partidas_completadas = len(historial)
total_correctas = sum(p["Correctas"] for p in historial)
total_incorrectas = sum(p["Incorrectas"] for p in historial)

if intentos_en_curso > 0 and not partida_guardada:
    total_correctas += puntaje_en_curso
    total_incorrectas += intentos_en_curso - puntaje_en_curso

total_respondidas = total_correctas + total_incorrectas
tasa_acierto = (total_correctas / total_respondidas * 100) if total_respondidas > 0 else 0.0

m1, m2, m3, m4 = st.columns(4)
m1.metric("🕹️ Partidas completadas", partidas_completadas)
m2.metric("✅ Respuestas correctas", total_correctas)
m3.metric("❌ Respuestas incorrectas", total_incorrectas)
m4.metric("🎯 Efectividad global", f"{tasa_acierto:.1f}%")

if total_respondidas == 0:
    st.info(
        "Aún no tienes registros de juego en esta sesión. Ve a la pestaña **Jugar** para "
        "responder preguntas y visualizar aquí tus estadísticas."
    )
else:
    col_tabla, col_graf = st.columns([1.3, 1])

    with col_tabla:
        st.markdown("#### Historial de rondas completadas (10 preguntas)")
        if historial:
            df_historial = pd.DataFrame(historial)
            st.dataframe(df_historial, use_container_width=True, hide_index=True)
        else:
            st.caption(
                f"Tienes una ronda en curso ({intentos_en_curso}/10 preguntas respondidas). "
                "Al completar las 10 preguntas aparecerá registrada en esta tabla."
            )

    with col_graf:
        st.markdown("#### Balance de respuestas")
        df_balance = pd.DataFrame(
            {
                "Resultado": ["Correctas", "Incorrectas"],
                "Cantidad": [total_correctas, total_incorrectas],
            }
        )
        fig = px.bar(
            df_balance,
            x="Resultado",
            y="Cantidad",
            color="Resultado",
            color_discrete_map={"Correctas": "#2E7D32", "Incorrectas": "#C62828"},
            text="Cantidad",
        )
        fig.update_layout(showlegend=False, height=300, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

    if st.button("🗑️ Limpiar historial de juego"):
        st.session_state["historial_juegos"] = []
        st.session_state["puntaje"] = 0
        st.session_state["intentos"] = 0
        st.session_state["partida_guardada"] = False
        st.rerun()