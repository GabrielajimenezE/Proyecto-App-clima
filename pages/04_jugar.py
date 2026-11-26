from datetime import datetime
import random
import streamlit as st
from src.data import cargar_datos

df = cargar_datos()
MAX_PREGUNTAS = 50

st.title("🎮 Desafío Climático IDEAM")
st.write(
    f"Responde **{MAX_PREGUNTAS} preguntas** sobre la geografía y las normales climatológicas "
    "de Colombia usando los registros reales de las estaciones meteorológicas."
)

if df.empty or "departamento" not in df.columns or "municipio" not in df.columns:
    st.warning("No se encontraron suficientes columnas en data/raw/datos.csv para iniciar el juego.")
    st.stop()

# 1. INICIALIZAR ESTADO DE SESIÓN Y HISTORIAL GLOBAL
if "puntaje" not in st.session_state:
    st.session_state["puntaje"] = 0
if "intentos" not in st.session_state:
    st.session_state["intentos"] = 0
if "respondido" not in st.session_state:
    st.session_state["respondido"] = False
if "partida_guardada" not in st.session_state:
    st.session_state["partida_guardada"] = False
if "historial_juegos" not in st.session_state:
    st.session_state["historial_juegos"] = []


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
col1.metric("🏆 Puntaje", f"{st.session_state['puntaje']} / {MAX_PREGUNTAS}")
col2.metric("🎯 Progreso", f"{st.session_state['intentos']} / {MAX_PREGUNTAS}")
precision = (
    (st.session_state["puntaje"] / st.session_state["intentos"] * 100)
    if st.session_state["intentos"] > 0
    else 0.0
)
col3.metric("📈 Precisión", f"{precision:.0f}%")

st.divider()

# 3. VALIDACIÓN DE FIN DE PARTIDA Y GUARDADO EN HISTORIAL
if st.session_state["intentos"] >= MAX_PREGUNTAS:
    if not st.session_state["partida_guardada"]:
        incorrectas = MAX_PREGUNTAS - st.session_state["puntaje"]
        st.session_state["historial_juegos"].append(
            {
                "Partida #": len(st.session_state["historial_juegos"]) + 1,
                "Hora": datetime.now().strftime("%H:%M:%S"),
                "Preguntas": MAX_PREGUNTAS,
                "Correctas": st.session_state["puntaje"],
                "Incorrectas": incorrectas,
                "Precisión (%)": round(precision, 1),
            }
        )
        st.session_state["partida_guardada"] = True

    st.success(
        f"🎉 ¡Partida finalizada! Lograste **{st.session_state['puntaje']} de {MAX_PREGUNTAS}** "
        f"aciertos ({precision:.0f}% de precisión). Tus estadísticas ya están disponibles en **Mis Datos**."
    )
    if st.button("🔄 Jugar otra ronda de 10 preguntas"):
        st.session_state["puntaje"] = 0
        st.session_state["intentos"] = 0
        st.session_state["partida_guardada"] = False
        generar_pregunta()
        st.rerun()
    st.stop()

# 4. TARJETA DE PREGUNTA ACTUAL
p = st.session_state["pregunta_actual"]
numero_actual = st.session_state["intentos"] + 1
st.subheader(
    f"📍 Pregunta {numero_actual} de {MAX_PREGUNTAS}: "
    f"¿En qué departamento se ubica la estación «{p['lugar']}»?"
)
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
        texto_btn = "🏁 Ver resultado final" if st.session_state["intentos"] >= MAX_PREGUNTAS else "➡️ Siguiente pregunta"
        if st.button(texto_btn):
            if st.session_state["intentos"] < MAX_PREGUNTAS:
                generar_pregunta()
            st.rerun()

# 5. REINICIAR PARTIDA EN CUALQUIER MOMENTO
st.divider()
if st.button("🔄 Reiniciar partida"):
    st.session_state["puntaje"] = 0
    st.session_state["intentos"] = 0
    st.session_state["partida_guardada"] = False
    generar_pregunta()
    st.rerun()