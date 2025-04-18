#poner mayusculas en tablas
import streamlit as st
import pandas as pd
from datetime import date

def mostrar_historial_diario():
    st.header("📆 Historial diario de aplicaciones")

    # Fecha a consultar
    fecha_consulta = st.date_input("Seleccionar fecha", value=date.today(), max_value=date.today())

    st.markdown("---")

    # Simulación de registros de vacunas (esto se reemplazará con Supabase)
    registros = [
        {"vacuna_id": 101, "vacuna": "COVID-19", "laboratorio": "Pfizer", "fecha": "2025-04-17"},
        {"vacuna_id": 102, "vacuna": "Triple Viral", "laboratorio": "Sinergium", "fecha": "2025-04-17"},
        {"vacuna_id": 101, "vacuna": "COVID-19", "laboratorio": "Pfizer", "fecha": "2025-04-17"},
        {"vacuna_id": 105, "vacuna": "Hepatitis B", "laboratorio": "Richmond", "fecha": "2025-04-16"},
    ]

    # Filtrar por fecha seleccionada
    fecha_str = fecha_consulta.strftime("%Y-%m-%d")
    filtrado = [r for r in registros if r["fecha"] == fecha_str]

    st.subheader("📊 Total de vacunas aplicadas:")
    st.success(f"{len(filtrado)} dosis registradas el {fecha_str}")

    st.markdown("---")

    # Filtros desplegables
    tipos_unicos = sorted({r["vacuna"] for r in registros})
    laboratorios_unicos = sorted({r["laboratorio"] for r in registros})

    tipo_filtro = st.selectbox("Filtrar por tipo de vacuna", ["Todas"] + tipos_unicos)
    nombre_filtro = st.selectbox("Filtrar por nombre de la vacuna", ["Todas"] + tipos_unicos)
    laboratorio_filtro = st.selectbox("Filtrar por laboratorio", ["Todos"] + laboratorios_unicos)

    if tipo_filtro != "Todas":
        filtrado = [r for r in filtrado if r["vacuna"] == tipo_filtro]
    if nombre_filtro != "Todas":
        filtrado = [r for r in filtrado if nombre_filtro.lower() in r["vacuna"].lower()]
    if laboratorio_filtro != "Todos":
        filtrado = [r for r in filtrado if laboratorio_filtro.lower() in r["laboratorio"].lower()]

    if filtrado:
        df = pd.DataFrame(filtrado)
        st.dataframe(df[["vacuna_id", "vacuna", "laboratorio"]], use_container_width=True)
    else:
        st.info("No se encontraron aplicaciones para la fecha seleccionada.")