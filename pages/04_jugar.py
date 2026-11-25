import random
import streamlit as st
from src.data import cargar_datos

df = cargar_datos()

st.title("🎮 Desafío Climático IDEAM")
st.write(
    "Pon a prueba tus conocimientos sobre la geografía y las normales climatológicas "
    "de Colombia usando los registros reales de las estaciones meteorológicas."
)

if df.empty or "departamento" not in df.columns or "municipio" not in df.columns:
    st.warning("No se encontraron suficientes columnas en data/raw/datos.csv para iniciar el juego.")
    st.stop()

# 1. INICIALIZAR ESTADO DE SESIÓN
if "puntaje" not in st.session_state:
    st.session_state["puntaje"] = 0
if "intentos" not in st.session_state:
    st.session_state["intentos"] = 0
if "respondido" not in st.session_state:
    st.session_state["respondido"] = False


def generar_pregunta():
    """Genera una pregunta aleatoria usando estaciones reales del dataset."""
    muestra = df.dropna(subset=["departamento", "municipio"]).sample(4)
    correcta = muestra.iloc[0]

    col_nombre = "estacion" if "estacion" in df.columns else "municipio"
    nombre_lugar = correcta[col_nombre]
    depto_correcto = correcta["departamento"]

    otros_deptos = (
        df[df["departamento"] != depto_correcto]["departamento"]
        .dropna()
        .unique()
        .tolist()
    )
    distractores = random.sample(otros_deptos, min(3, len(otros_deptos)))
    opciones = distractores + [depto_correcto]
    random.shuffle(opciones)

    st.session_state["pregunta_actual"] = {
        "lugar": nombre_lugar,
        "municipio": correcta["municipio"],
        "altitud": correcta.get("altitud_m", "N/D"),
        "respuesta_correcta": depto_correcto,
        "opciones": opciones,
    }
    st.session_state["respondido"] = False


if "pregunta_actual" not in st.session_state:
    generar_pregunta()

# 2. MARCADOR SUPERIOR
col1, col2, col3 = st.columns(3)
col1.metric("🏆 Puntaje", st.session_state["puntaje"])
col2.metric("🎯 Intentos", st.session_state["intentos"])
precision = (
    (st.session_state["puntaje"] / st.session_state["intentos"] * 100)
    if st.session_state["intentos"] > 0
    else 0.0
)
col3.metric("📈 Precisión", f"{precision:.0f}%")

st.divider()

# 3. TARJETA DE PREGUNTA
p = st.session_state["pregunta_actual"]
st.subheader(f"📍 ¿En qué departamento se ubica la estación «{p['lugar']}»?")
st.caption(f"Pista: Pertenece al municipio de **{p['municipio']}** (Altitud: {p['altitud']} m s. n. m.)")

seleccion = st.radio(
    "Selecciona una respuesta:",
    p["opciones"],
    index=None,
    disabled=st.session_state["respondido"],
)

col_btn1, col_btn2 = st.columns([1, 3])

with col_btn1:
    if st.button("✅ Validar respuesta", disabled=st.session_state["respondido"] or seleccion is None):
        st.session_state["respondido"] = True
        st.session_state["intentos"] += 1
        if seleccion == p["respuesta_correcta"]:
            st.session_state["puntaje"] += 1
            st.balloons()
            st.success(f"¡Correcto! La estación {p['lugar']} está en **{p['respuesta_correcta']}**.")
        else:
            st.error(f"Incorrecto. La respuesta correcta era **{p['respuesta_correcta']}**.")

with col_btn2:
    if st.session_state["respondido"]:
        if st.button("➡️ Siguiente pregunta"):
            generar_pregunta()
            st.rerun()

# 4. REINICIAR PARTIDA
st.divider()
if st.button("🔄 Reiniciar marcador"):
    st.session_state["puntaje"] = 0
    st.session_state["intentos"] = 0
    generar_pregunta()
    st.rerun()