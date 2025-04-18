import streamlit as st
import pandas as pd
from datetime import date
import calendar
import matplotlib.pyplot as plt

def mostrar_historial_mensual():
    st.header("🗓️ Historial mensual de aplicaciones")

    # Selección de mes y año
    hoy = date.today()
    anio = st.selectbox("Seleccionar año", list(range(hoy.year, hoy.year - 5, -1)))
    mes = st.selectbox("Seleccionar mes", list(calendar.month_name)[1:])
    mes_num = list(calendar.month_name).index(mes)

    st.markdown("---")

    # Simulación de registros de vacunas
    registros = [
        {"vacuna_id": 101, "vacuna": "COVID-19", "laboratorio": "Pfizer", "fecha": "2025-04-01"},
        {"vacuna_id": 101, "vacuna": "COVID-19", "laboratorio": "Pfizer", "fecha": "2025-04-03"},
        {"vacuna_id": 102, "vacuna": "Triple Viral", "laboratorio": "Sinergium", "fecha": "2025-04-07"},
        {"vacuna_id": 105, "vacuna": "Hepatitis B", "laboratorio": "Richmond", "fecha": "2025-04-15"},
        {"vacuna_id": 104, "vacuna": "Antigripal", "laboratorio": "Sinergium", "fecha": "2025-04-21"},
        {"vacuna_id": 101, "vacuna": "COVID-19", "laboratorio": "Moderna", "fecha": "2025-04-30"},
    ]

    registros_mes = [r for r in registros if date.fromisoformat(r["fecha"]).month == mes_num and date.fromisoformat(r["fecha"]).year == anio]

    st.subheader("📊 Total de vacunas aplicadas:")
    st.success(f"{len(registros_mes)} dosis registradas en {mes} {anio}")

    st.markdown("---")

    tipos_unicos = sorted({r["vacuna"] for r in registros_mes})
    laboratorios_unicos = sorted({r["laboratorio"] for r in registros_mes})

    tipo_filtro = st.selectbox("Filtrar por tipo de vacuna", ["Todas"] + tipos_unicos)
    nombre_filtro = st.selectbox("Filtrar por nombre de la vacuna", ["Todas"] + tipos_unicos)
    laboratorio_filtro = st.selectbox("Filtrar por laboratorio", ["Todos"] + laboratorios_unicos)

    filtrado = registros_mes
    if tipo_filtro != "Todas":
        filtrado = [r for r in filtrado if r["vacuna"] == tipo_filtro]
    if nombre_filtro != "Todas":
        filtrado = [r for r in filtrado if nombre_filtro.lower() in r["vacuna"].lower()]
    if laboratorio_filtro != "Todos":
        filtrado = [r for r in filtrado if laboratorio_filtro.lower() in r["laboratorio"].lower()]

    if filtrado:
        df = pd.DataFrame(filtrado)
        st.dataframe(df[["vacuna_id", "vacuna", "laboratorio", "fecha"]], use_container_width=True)

        # Gráfico: aplicaciones por tipo de vacuna y laboratorio
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Aplicaciones por tipo de vacuna")
            fig1, ax1 = plt.subplots()
            df["vacuna"].value_counts().plot(kind="bar", ax=ax1, color="#00449E")
            ax1.set_ylabel("Cantidad de dosis")
            ax1.set_xlabel("Tipo de vacuna")
            st.pyplot(fig1)

        with col2:
            st.subheader("🧪 Aplicaciones por laboratorio")
            fig2, ax2 = plt.subplots()
            df["laboratorio"].value_counts().plot(kind="bar", ax=ax2, color="#3CB371")
            ax2.set_ylabel("Cantidad de dosis")
            ax2.set_xlabel("Laboratorio")
            st.pyplot(fig2)
    else:
        st.info("No se encontraron aplicaciones para el mes seleccionado.")
