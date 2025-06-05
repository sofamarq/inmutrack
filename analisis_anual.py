import streamlit as st
import pandas as pd
import calendar
import matplotlib.pyplot as plt
from datetime import date
from funciones_supabase import obtener_aplicaciones_anuales

#     # Datos simulados
#     registros = [
#         {"vacuna": "COVID-19", "laboratorio": "Pfizer", "fecha": "2025-01-15"},
#         {"vacuna": "COVID-19", "laboratorio": "Moderna", "fecha": "2025-02-10"},
#         {"vacuna": "Triple Viral", "laboratorio": "Sinergium", "fecha": "2025-03-05"},
#         {"vacuna": "Antigripal", "laboratorio": "Sinergium", "fecha": "2025-03-20"},
#         {"vacuna": "Hepatitis B", "laboratorio": "Richmond", "fecha": "2025-04-15"},
#         {"vacuna": "Antigripal", "laboratorio": "Sinergium", "fecha": "2025-05-20"},
#         {"vacuna": "COVID-19", "laboratorio": "Moderna", "fecha": "2025-06-12"},
#         {"vacuna": "Triple Viral", "laboratorio": "Sinergium", "fecha": "2025-07-09"},
#         {"vacuna": "Hepatitis B", "laboratorio": "Richmond", "fecha": "2025-08-30"},
#         {"vacuna": "Antigripal", "laboratorio": "Sinergium", "fecha": "2025-09-14"},
#         {"vacuna": "COVID-19", "laboratorio": "Pfizer", "fecha": "2025-10-18"},
#         {"vacuna": "Triple Viral", "laboratorio": "Sinergium", "fecha": "2025-11-22"},
#         {"vacuna": "Hepatitis B", "laboratorio": "Richmond", "fecha": "2025-12-05"}
#     ]


def mostrar_analisis_anual():
    st.header("📅 Análisis anual de vacunación")

    hoy = date.today()
    anio = st.selectbox("Seleccionar año", list(range(hoy.year, hoy.year - 5, -1)))
    id_centro = st.session_state.get("id_centro", None)

    if id_centro is None:
        st.warning("No se encontró el centro en sesión.")
        return

    resultado = obtener_aplicaciones_anuales(anio, id_centro)

    if not resultado or not resultado.data:
        st.info("No se encontraron registros para el año seleccionado.")
        return

    registros = [
        {
            "Fecha": r["fecha_aplicacion"],
            "Vacuna": r["vacunas"]["nombre_vacuna"] if r.get("vacunas") else "",
            "Laboratorio": r["vacunas"]["laboratorio"] if r.get("vacunas") else ""
        }
        for r in resultado.data
    ]

    df = pd.DataFrame(registros)
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df["mes"] = df["Fecha"].dt.month
    df.index = df.index + 1

    # Solapas
    tab1, tab2 = st.tabs(["📊 Análisis", "📋 Ver historial detallado"])

    with tab1:
        st.subheader(f"Total de dosis aplicadas en {anio}:")
        st.success(f"{len(df)} aplicaciones registradas")

        # Gráfico mensual
        resumen_mes = df.groupby("mes").size().reindex(range(1, 13), fill_value=0)
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        resumen_mes.plot(kind="line", color="#FF7F50", marker='o', ax=ax1)
        ax1.axhline(resumen_mes.mean(), linestyle='--', color='gray', label='Promedio')
        #ax1.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)], rotation=45)
        ax1.set_xticks(range(1, 13))
        ax1.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)], rotation=45)
        ax1.set_ylabel("Aplicaciones")
        ax1.grid(True, linestyle='--', alpha=0.6)
        ax1.legend()
        st.pyplot(fig1)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Por tipo de vacuna")
            fig2, ax2 = plt.subplots()
            df["Vacuna"].value_counts().plot(kind="bar", color="#00449E", ax=ax2)
            ax2.set_ylabel("Dosis")
            st.pyplot(fig2)

        with col2:
            st.subheader("Por laboratorio")
            fig3, ax3 = plt.subplots()
            df["Laboratorio"].value_counts().plot(kind="bar", color="#3CB371", ax=ax3)
            ax3.set_ylabel("Dosis")
            st.pyplot(fig3)

        # Ranking
        
        st.subheader("Ranking de vacunas más aplicadas")
        ranking = df["Vacuna"].value_counts().reset_index()
        ranking.columns = ["Vacuna", "Aplicaciones"]
        #Iniciar índice en 1 y renombrar la columna del índice a "N°"
        ranking.index = ranking.index + 1
        ranking.index.name = "N°"
        st.dataframe(ranking, use_container_width=True)



    with tab2:
        st.subheader("📋 Historial de aplicaciones en el año")

        filtro_vacuna = st.selectbox("Filtrar por vacuna", ["Todas"] + sorted(df["Vacuna"].unique()))
        filtro_laboratorio = st.selectbox("Filtrar por laboratorio", ["Todos"] + sorted(df["Laboratorio"].unique()))
        filtro_mes = st.selectbox("Filtrar por mes", ["Todos"] + [calendar.month_name[m] for m in sorted(df["mes"].unique())])

        df_filtrado = df.copy()
        df_filtrado["Fecha"] = pd.to_datetime(df_filtrado["Fecha"]).dt.strftime("%Y-%m-%d")
        if filtro_vacuna != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Vacuna"] == filtro_vacuna]
        if filtro_laboratorio != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Laboratorio"] == filtro_laboratorio]
        if filtro_mes != "Todos":
            mes_num = list(calendar.month_name).index(filtro_mes)
            df_filtrado = df_filtrado[df_filtrado["mes"] == mes_num]

        st.dataframe(df_filtrado[["Fecha", "Vacuna", "Laboratorio"]].sort_values("Fecha"), use_container_width=True)