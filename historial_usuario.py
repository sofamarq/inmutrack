#Falta hacer la conexion. Me gusta como quedo. Tiene un indice que queda feo con esto pero es por como estan cargadas los datos ficticios


import streamlit as st
import pandas as pd
#from supabase_usuario import obtener_historial_vacunacion_usuario

# Simulación de función hasta conectar con Supabase
def obtener_historial_vacunacion_usuario(dni):
    # Datos ficticios para pruebas
    return [
        {
            "Vacuna": "Sputnik V",
            "Laboratorio": "Gamaleya",
            "Enfermedad": "COVID-19",
            "Fecha": "2021-03-15",
            "Dosis": "Primera dosis"
        },
        {
            "Vacuna": "Sputnik V",
            "Laboratorio": "Gamaleya",
            "Enfermedad": "COVID-19",
            "Fecha": "2021-04-15",
            "Dosis": "Segunda dosis"
        },
        {
            "Vacuna": "Triple Viral",
            "Laboratorio": "Sinergium",
            "Enfermedad": "Sarampión",
            "Fecha": "2010-05-10",
            "Dosis": "Única dosis"
        },
        {
            "Vacuna": "Antigripal",
            "Laboratorio": "Sanofi",
            "Enfermedad": "Influenza",
            "Fecha": "2023-06-20",
            "Dosis": "Anual"
        }
    ]

def mostrar_historial_usuario():
    st.header("📋 Historial de vacunación")

    dni = st.session_state.get("dni", "12345678")  # para pruebas

    registros = obtener_historial_vacunacion_usuario(dni)

    if not registros:
        st.info("No se encontraron registros de vacunación.")
        return

    df = pd.DataFrame(registros)
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df = df.sort_values("Fecha", ascending=True)

    #st.markdown("### Filtros") #esto pone un subtitulo de filtros
    filtro_enfermedad = st.selectbox("Filtrar por enfermedad", options=["Todas"] + sorted(df["Enfermedad"].unique().tolist()))
    if filtro_enfermedad != "Todas":
        df = df[df["Enfermedad"] == filtro_enfermedad]

    if st.toggle("Ordenar por fecha más reciente primero"):
        df = df.sort_values("Fecha", ascending=False)

    st.dataframe(df[["Vacuna", "Laboratorio", "Enfermedad", "Fecha", "Dosis"]], use_container_width=True)


