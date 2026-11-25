import streamlit as st
from src.data import cargar_datos, filtrar_datos
import src.figuras as fig

df = cargar_datos()

if "estaciones_favoritas" not in st.session_state:
    st.session_state["estaciones_favoritas"] = []

st.title("🔍 Explorar Datos Climáticos")
st.write("Filtra por departamento, municipio o estación y haz clic sobre una fila para ver su ficha detallada.")

if not df.empty:
    # FILTROS EN COLUMNAS
    col1, col2, col3 = st.columns(3)
    with col1:
        departamentos = ["Todos"] + sorted(df["departamento"].dropna().unique().tolist()) if "departamento" in df.columns else ["Todos"]
        dep_seleccionado = st.selectbox("🗺️ Departamento", departamentos)
    with col2:
        muni_buscar = st.text_input("🏙️ Municipio", placeholder="Ej. Medellín")
    with col3:
        est_buscar = st.text_input("📡 Estación", placeholder="Nombre de estación...")

    df_filtrado = filtrar_datos(
        df,
        estacion=est_buscar,
        departamento=dep_seleccionado,
        municipio=muni_buscar,
    )

    # TABLA SELECCIONABLE (Igual al ejemplo de la profesora)
    st.divider()
    st.subheader(f"Registros encontrados: {len(df_filtrado):,}")

    evento = st.dataframe(
        df_filtrado,
        on_select="rerun",
        selection_mode="single-row",
        hide_index=True,
        use_container_width=True,
    )

    # DETALLE DE LA FILA SELECCIONADA
    if evento["selection"]["rows"]:
        st.divider()
        fila = df_filtrado.iloc[evento["selection"]["rows"][0]]
        st.subheader("📌 Detalle de la Estación Seleccionada")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.write(f"**Departamento:** {fila.get('departamento', 'N/A')}")
            st.write(f"**Municipio:** {fila.get('municipio', 'N/A')}")
        with c2:
            if "precipitacion_anual_mm" in fila:
                st.metric("🌧️ Precipitación Anual", f"{fila['precipitacion_anual_mm']:.1f} mm")
        with c3:
            if st.button("⭐ Guardar estación en favoritos"):
                etiqueta = f"{fila.get('municipio', 'Estación')} ({fila.get('departamento', '')})"
                if etiqueta not in st.session_state["estaciones_favoritas"]:
                    st.session_state["estaciones_favoritas"].append(etiqueta)
                    st.success(f"Guardada: {etiqueta}")

        if st.session_state["estaciones_favoritas"]:
            st.write("**Estaciones guardadas en esta sesión:**", st.session_state["estaciones_favoritas"])
    else:
        st.info("👆 Selecciona una fila en la tabla para inspeccionar los detalles de la estación.")

    # GRÁFICOS MODULARES DESDE src/figuras.py
    st.divider()
    if "departamento" in df_filtrado.columns:
        st.plotly_chart(fig.estaciones_por_departamento(df_filtrado), use_container_width=True)

    if "precipitacion_anual_mm" in df_filtrado.columns:
        st.plotly_chart(fig.histograma_precipitacion(df_filtrado), use_container_width=True)

    graf_disp = fig.relacion_variables(df_filtrado)
    if graf_disp is not None:
        st.plotly_chart(graf_disp, use_container_width=True)
else:
    st.warning("No se encontraron datos para mostrar. Verifica que data/raw/datos.csv exista.")