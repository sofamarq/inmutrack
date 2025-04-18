import streamlit as st
import pandas as pd
import calendar
import matplotlib.pyplot as plt
from datetime import date

def mostrar_analisis_anual():
    st.header("📅 Análisis anual de vacunación")

    hoy = date.today()
    anio = st.selectbox("Seleccionar año", list(range(hoy.year, hoy.year - 5, -1)))

    # Solapa de historial detallado
    tab1, tab2 = st.tabs(["📊 Análisis", "📋 Ver historial detallado"])

    # Datos simulados
    registros = [
        {"vacuna": "COVID-19", "laboratorio": "Pfizer", "fecha": "2025-01-15"},
        {"vacuna": "COVID-19", "laboratorio": "Moderna", "fecha": "2025-02-10"},
        {"vacuna": "Triple Viral", "laboratorio": "Sinergium", "fecha": "2025-03-05"},
         {"vacuna": "Antigripal", "laboratorio": "Sinergium", "fecha": "2025-03-20"},
        {"vacuna": "Hepatitis B", "laboratorio": "Richmond", "fecha": "2025-04-15"},
        {"vacuna": "Antigripal", "laboratorio": "Sinergium", "fecha": "2025-05-20"},
        {"vacuna": "COVID-19", "laboratorio": "Moderna", "fecha": "2025-06-12"},
        {"vacuna": "Triple Viral", "laboratorio": "Sinergium", "fecha": "2025-07-09"},
        {"vacuna": "Hepatitis B", "laboratorio": "Richmond", "fecha": "2025-08-30"},
        {"vacuna": "Antigripal", "laboratorio": "Sinergium", "fecha": "2025-09-14"},
        {"vacuna": "COVID-19", "laboratorio": "Pfizer", "fecha": "2025-10-18"},
        {"vacuna": "Triple Viral", "laboratorio": "Sinergium", "fecha": "2025-11-22"},
        {"vacuna": "Hepatitis B", "laboratorio": "Richmond", "fecha": "2025-12-05"}
    ]

    df = pd.DataFrame([r for r in registros if pd.to_datetime(r["fecha"]).year == anio])

    if df.empty:
        st.info("No se encontraron registros para el año seleccionado.")
        return

    with tab1:
        st.subheader(f"Total de dosis aplicadas en {anio}:")
        st.success(f"{len(df)} aplicaciones registradas")

        st.markdown("---")

        # Aplicaciones por mes
        st.subheader("Distribución mensual")
        df["mes"] = pd.to_datetime(df["fecha"]).dt.month
        resumen_mes = df.groupby("mes").size().reindex(range(1, 13), fill_value=0)
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        resumen_mes.plot(kind="line", color="#FF7F50", marker='o', ax=ax1)
        ax1.grid(True, linestyle='--', alpha=0.6)
        promedio = resumen_mes.mean()
        ax1.axhline(promedio, linestyle='--', color='gray', label=f'Promedio: {promedio:.1f}')
        ax1.legend()
        ax1.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)], rotation=45)
        ax1.set_yticks([i * 0.5 for i in range(int(resumen_mes.max()*2)+2)])
        ax1.set_ylabel("Aplicaciones")
        st.pyplot(fig1, use_container_width=False)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Por tipo de vacuna")
            fig2, ax2 = plt.subplots()
            df["vacuna"].value_counts().plot(kind="bar", color="#00449E", ax=ax2)
            ax2.set_ylabel("Dosis")
            st.pyplot(fig2)

        with col2:
            st.subheader("Por laboratorio")
            fig3, ax3 = plt.subplots()
            df["laboratorio"].value_counts().plot(kind="bar", color="#3CB371", ax=ax3)
            ax3.set_ylabel("Dosis")
            st.pyplot(fig3)

        # Ranking
        st.markdown("---")
        st.subheader("Ranking de vacunas más aplicadas")
        ranking = df["vacuna"].value_counts().reset_index()
        ranking.columns = ["Vacuna", "Aplicaciones"]
        st.dataframe(ranking, use_container_width=True)

    

    
    with tab2:
        st.subheader("📋 Historial de aplicaciones en el año")

        filtro_vacuna = st.selectbox("Filtrar por vacuna", ["Todas"] + sorted(df["vacuna"].unique()))
        filtro_laboratorio = st.selectbox("Filtrar por laboratorio", ["Todos"] + sorted(df["laboratorio"].unique()))
        filtro_mes = st.selectbox("Filtrar por mes", ["Todos"] + [calendar.month_name[i] for i in sorted(df["mes"].unique())])

        df_filtrado = df.copy()
        if filtro_vacuna != "Todas":
            df_filtrado = df_filtrado[df_filtrado["vacuna"] == filtro_vacuna]
        if filtro_laboratorio != "Todos":
            df_filtrado = df_filtrado[df_filtrado["laboratorio"] == filtro_laboratorio]
        if filtro_mes != "Todos":
            mes_num = list(calendar.month_name).index(filtro_mes)
            df_filtrado = df_filtrado[df_filtrado["mes"] == mes_num]

        st.dataframe(df_filtrado[["fecha", "vacuna", "laboratorio"]].sort_values("fecha"), use_container_width=True)
