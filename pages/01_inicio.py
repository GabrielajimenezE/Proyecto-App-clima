import os
import streamlit as st

# 1. TÍTULO Y DESCRIPCIÓN GENERAL
st.title("🌦️ EcoClima 360")
st.subheader("Descripción General")
st.markdown(
    """
    **EcoClima 360** es una plataforma web interactiva desarrollada en **Streamlit** para la 
    visualización, exploración y análisis lúdico de registros meteorológicos y climáticos. 
    La aplicación permite a los usuarios consultar datos históricos de temperatura, humedad y 
    precipitaciones, descubrir patrones mediante visualizaciones dinámicas y participar en un 
    juego interactivo de predicción climática.
    """
)

# 2. REPORTE DE VISIÓN
st.markdown("### 🎯 Reporte de Visión")
st.write(
    "Proporcionar a estudiantes, investigadores y ciudadanos una herramienta accesible e intuitiva "
    "para visualizar y comprender las variables climatológicas registradas por el IDEAM en los "
    "diferentes departamentos de Colombia."
)

col_v1, col_v2 = st.columns(2)
with col_v1:
    st.info(
        "**Objetivo**\n\n"
        "Facilitar el acceso y la comprensión de datos climáticos mediante herramientas "
        "interactivas de análisis y dinámicas de gamificación."
    )
with col_v2:
    st.info(
        "**Beneficios**\n\n"
        "Promover la educación ambiental y el análisis de datos de manera accesible e "
        "intuitiva para usuarios no expertos y estudiantes."
    )

st.divider()

# 3. EQUIPO DE TRABAJO (3 INTEGRANTES)
st.markdown("### 👥 Equipo de Trabajo")

integrantes = [
    {
        "nombre": "Evelis Gabriela Jiménez Estrada",
        "rol": "Coordinación y Administración de GitHub",
        "foto": "assets/gabriela.jpeg",
        "bio": (
            "Soy estudiante de Ingeniería Industrial de la Universidad de Antioquia. Me interesa "
            "aprender sobre nuevas herramientas y poner en práctica mis conocimientos en proyectos "
            "que me permitan fortalecer mis habilidades. Me gusta trabajar en equipo, aportar ideas "
            "y asumir nuevos retos. En este proyecto estoy encargada de coordinar las actividades "
            "del equipo y administrar el repositorio de GitHub, apoyando la organización y el "
            "seguimiento del trabajo."
        ),
    },
    {
        "nombre": "Brayan Ardany Pérez Cardona",
        "rol": "Gestión, Limpieza y Validación de Datos",
        "foto": "assets/brayan.jpeg",
        "bio": (
            "Tengo 31 años y soy estudiante de Ingeniería Industrial en la Universidad de Antioquia. "
            "Cuento con sólidas habilidades en herramientas ofimáticas y actualmente me desempeño "
            "como auxiliar comercial de proyectos en una empresa de iluminación, experiencia que me "
            "ha permitido desarrollar organización, análisis y orientación a resultados. En "
            "**EcoClima 360** estoy dispuesto a aportar de manera integral en todos los ámbitos del "
            "equipo, asumiendo como función principal la gestión, limpieza y validación de los datos."
        ),
    },
    {
        "nombre": "Yeison Enrique López Mosquera",
        "rol": "Investigación, Documentación Técnica y Pruebas",
        "foto": "assets/yeison.jpeg",
        "bio": (
            "Tengo 28 años y soy estudiante de Ingeniería Industrial de la Universidad de Antioquia. "
            "Cuento con conocimientos y habilidades en Excel, Python y gestión logística, enfocado "
            "en la optimización de procesos y el análisis estructurado de la información. Dentro del "
            "proyecto desempeño el rol de **investigador de aplicación, documentación técnica y "
            "pruebas**, asegurando la calidad y claridad funcional de la herramienta."
        ),
    },
]

cols = st.columns(3)

for col, persona in zip(cols, integrantes):
    with col:
        with st.container(border=True):
            if os.path.exists(persona["foto"]):
                st.image(persona["foto"], width=150)
            else:
                st.warning(f"No se encontró la imagen: `{persona['foto']}`")
            st.markdown(f"#### {persona['nombre']}")
            st.caption(f"**{persona['rol']}**")
            st.write(persona["bio"])

st.divider()

# 4. LICENCIA Y CRÉDITOS
st.caption(
    "**Licencia y Créditos:** Este proyecto está bajo la licencia **Creative Commons "
    "Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. Consultar el archivo "
    "`docs/LICENSE.md` para más detalles."
)