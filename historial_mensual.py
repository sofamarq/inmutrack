import streamlit as st
import pandas as pd
from datetime import date
import calendar
import matplotlib.pyplot as plt
from funciones_supabase import obtener_aplicaciones_por_mes

def mostrar_historial_mensual():
    st.header("🗓️ Historial mensual de aplicaciones")

    # Selección de mes y año
    hoy = date.today()
    anio = st.selectbox("Seleccionar año", list(range(hoy.year, hoy.year - 5, -1)))
    mes = st.selectbox("Seleccionar mes", list(calendar.month_name)[1:])
    mes_num = list(calendar.month_name).index(mes)

    st.markdown("---")

    # ID del centro desde sesión
    id_centro = st.session_state.get("id_centro", 0)

    # Obtener datos reales (ya devuelve una lista de registros enriquecidos)
    registros = obtener_aplicaciones_por_mes(anio, mes_num, id_centro)

    if not registros:
        st.warning("No se encontraron aplicaciones.")
        return

    # Convertir a DataFrame
    df = pd.DataFrame([
        {
            "ID Vacuna": r["id_vacuna"],
            "Vacuna": r["nombre_vacuna"],
            "Laboratorio": r["laboratorio"],
            "Fecha": r["fecha_aplicacion"]
        }
        for r in registros
    ])

    df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m-%d")

    st.subheader("📊 Total de vacunas aplicadas:")
    st.success(f"{len(df)} dosis registradas en {mes} {anio}")

    st.markdown("---")

    tipos_unicos = sorted(df["Vacuna"].unique())
    laboratorios_unicos = sorted(df["Laboratorio"].unique())

    tipo_filtro = st.selectbox("Filtrar por tipo de vacuna", ["Todas"] + tipos_unicos)
    nombre_filtro = st.selectbox("Filtrar por nombre de la vacuna", ["Todas"] + tipos_unicos)
    laboratorio_filtro = st.selectbox("Filtrar por laboratorio", ["Todos"] + laboratorios_unicos)

    df_filtrado = df.copy()

    if tipo_filtro != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Vacuna"] == tipo_filtro]
    if nombre_filtro != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Vacuna"].str.contains(nombre_filtro, case=False)]
    if laboratorio_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Laboratorio"].str.contains(laboratorio_filtro, case=False)]

    if not df_filtrado.empty:
        st.dataframe(df_filtrado[["ID Vacuna", "Vacuna", "Laboratorio", "Fecha"]], use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Aplicaciones por tipo de vacuna")
            fig1, ax1 = plt.subplots()
            df_filtrado["Vacuna"].value_counts().plot(kind="bar", ax=ax1, color="#00449E")
            ax1.set_ylabel("Cantidad de dosis")
            ax1.set_xlabel("Tipo de vacuna")
            st.pyplot(fig1)

        with col2:
            st.subheader("🧪 Aplicaciones por laboratorio")
            fig2, ax2 = plt.subplots()
            df_filtrado["Laboratorio"].value_counts().plot(kind="bar", ax=ax2, color="#3CB371")
            ax2.set_ylabel("Cantidad de dosis")
            ax2.set_xlabel("Laboratorio")
            st.pyplot(fig2)
    else:
        st.info("No se encontraron aplicaciones para el mes seleccionado.")
