import plotly.express as px


def estaciones_por_departamento(df):
    df_conteo = df["departamento"].value_counts().reset_index()
    df_conteo.columns = ["departamento", "count"]

    grafico = px.bar(
        df_conteo.head(15),
        y="departamento",
        x="count",
        title="📍 Cantidad de estaciones por Departamento (Top 15)",
        labels={"departamento": "", "count": "Cantidad de estaciones"},
        color="count",
        color_continuous_scale="Tealgrn",
    )
    grafico.update_layout(coloraxis_showscale=False)
    return grafico


def histograma_precipitacion(df):
    grafico = px.histogram(
        df,
        x="precipitacion_anual_mm",
        title="🌧️ Distribución de Precipitación Anual (mm)",
        labels={"precipitacion_anual_mm": "Precipitación Anual (mm)"},
    )
    grafico.update_layout(hovermode="x unified")
    grafico.update_yaxes(title_text="Cantidad de estaciones")
    grafico.update_traces(marker_color="#2E8B57")
    return grafico


def relacion_variables(df):
    col_x = next(
        (c for c in ["altitud_m", "altitud", "elevacion", "temperatura_media"] if c in df.columns),
        None,
    )
    if col_x and "precipitacion_anual_mm" in df.columns:
        hover_col = "municipio" if "municipio" in df.columns else None
        grafico = px.scatter(
            df,
            x=col_x,
            y="precipitacion_anual_mm",
            hover_name=hover_col,
            title=f"🌦️ {col_x.replace('_', ' ').title()} vs. Precipitación Anual",
            labels={
                col_x: "Altitud (m s. n. m.)" if col_x == "altitud_m" else col_x,
                "precipitacion_anual_mm": "Precipitación Anual (mm)",
            },
            color="precipitacion_anual_mm",
            color_continuous_scale="Turbo",
        )
        grafico.update_layout(coloraxis_showscale=False)
        return grafico
    return None