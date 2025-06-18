import streamlit as st
import pandas as pd
from funciones_supabase import obtener_historial_vacunacion_usuario

def mostrar_historial_usuario():
    st.header("📋 Historial de vacunación")

    dni = st.session_state.get("dni")  # debe haberse guardado al ingresar

    if not dni:
        st.warning("No se encontró DNI en sesión.")
        return

    registros = obtener_historial_vacunacion_usuario(int(dni))

    if not registros or len(registros) == 0:
        st.info("No se encontraron registros de vacunación.")
        return

    df = pd.DataFrame([
        {
            "Vacuna": r.get("vacuna", ""),
            "Laboratorio": r.get("laboratorio", ""),
            "Enfermedad": r.get("enfermedad", ""),
            "Fecha": r.get("fecha", "")
        }
        for r in registros
    ])

    df.index = df.index + 1
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df = df.sort_values("Fecha", ascending=True)
    df["Fecha"] = df["Fecha"].dt.strftime("%Y-%m-%d")


    filtro_enfermedad = st.selectbox("Filtrar por enfermedad", options=["Todas"] + sorted(df["Enfermedad"].unique().tolist()))
    if filtro_enfermedad != "Todas":
        df = df[df["Enfermedad"] == filtro_enfermedad]

    if st.toggle("Ordenar por fecha más reciente primero"):
        df = df.sort_values("Fecha", ascending=False)

    st.dataframe(df[["Vacuna", "Laboratorio", "Enfermedad", "Fecha"]], use_container_width=True)
