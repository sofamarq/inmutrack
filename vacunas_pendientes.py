import streamlit as st
import pandas as pd
from datetime import datetime
from envio_mail import enviar_recordatorio_vacunas


# --- Simulaciones hasta conectar con Supabase ---
def obtener_datos_usuario():
    return {
        "dni": "12345678",
        "fecha_nacimiento": "2000-05-15",
        "personal_salud": True,
        "embarazada": False
    }

def obtener_historial_vacunacion_usuario(dni):
    return [
        {"vacuna": "BCG", "fecha": "2000-05-20"},
        {"vacuna": "Triple Viral", "fecha": "2010-06-01"},
        {"vacuna": "COVID-19", "fecha": "2021-04-15"},
        {"vacuna": "COVID-19", "fecha": "2022-05-15"},
        {"vacuna": "Antigripal", "fecha": "2023-06-20"}
    ]

def obtener_vacunas():
    return pd.DataFrame([
        {"vacuna": "BCG", "edad_1ra": 0, "refuerzo": None, "grupo": None, "obligatoria": True},
        {"vacuna": "Hepatitis B", "edad_1ra": 0, "refuerzo": None, "grupo": "personal_salud", "obligatoria": True},
        {"vacuna": "Triple Viral", "edad_1ra": 12, "refuerzo": 60, "grupo": None, "obligatoria": True},
        {"vacuna": "COVID-19", "edad_1ra": 180, "refuerzo": 12, "grupo": None, "obligatoria": True},
        {"vacuna": "Antigripal", "edad_1ra": 6, "refuerzo": 12, "grupo": "embarazada", "obligatoria": False},
        {"vacuna": "Antigripal", "edad_1ra": 780, "refuerzo": 12, "grupo": "personal_salud", "obligatoria": False}
    ])


# --- Lógica principal ---
def mostrar_vacunas_pendientes():
    st.header("🧾 Vacunas pendientes")

    usuario = obtener_datos_usuario()
    historial = obtener_historial_vacunacion_usuario(usuario["dni"])
    vacunas = obtener_vacunas()

    edad_hoy = (datetime.today() - datetime.strptime(usuario["fecha_nacimiento"], "%Y-%m-%d")).days // 30  # en meses
    edad_proximo_anio = edad_hoy + 12

    aplicadas = [v["vacuna"] for v in historial]
    pendientes = []
    proximas = []
    completadas = []

    for _, row in vacunas.iterrows():
        if row["grupo"] and not usuario.get(row["grupo"], False):
            continue

        recibidas = [v for v in historial if v["vacuna"] == row["vacuna"]]

        if row["edad_1ra"] <= edad_hoy:
            if not recibidas:
                pendientes.append(row["vacuna"])
            else:
                completadas.append(row["vacuna"])

        if row["refuerzo"] and row["edad_1ra"] <= edad_proximo_anio < row["edad_1ra"] + row["refuerzo"]:
            proximas.append(row["vacuna"])

    # Filtro por tipo de vacuna
    filtro_tipo = st.selectbox("Filtrar por tipo de vacuna", ["Todas", "Obligatoria", "Sugerida"])

    # Mostrar tabla resumen
    st.subheader("📊 Resumen de estado de vacunación")
    df_estado = pd.DataFrame([
        {
            "Vacuna": v,
            "Estado": ("Pendiente" if v in pendientes else ("Próxima" if v in proximas else "Aplicada")),
            "Tipo": ("Obligatoria" if vacunas[vacunas["vacuna"] == v]["obligatoria"].iloc[0] else "Sugerida")
        } for v in sorted(set(pendientes + completadas + proximas))
    ])
    if filtro_tipo != "Todas":
        df_estado = df_estado[df_estado["Tipo"] == filtro_tipo]

    st.dataframe(df_estado, use_container_width=True)

    # Vista en columnas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚨 Vacunas pendientes")
        if pendientes:
            for v in pendientes:
                tipo = "(Obligatoria)" if vacunas[vacunas["vacuna"] == v]["obligatoria"].iloc[0] else "(Sugerida)"
                st.markdown(f"- {v} {tipo}")
        else:
            st.success("No hay vacunas pendientes 🎉")

    with col2:
        st.subheader("📅 Próximas vacunas")
        if proximas:
            for v in proximas:
                tipo = "(Obligatoria)" if vacunas[vacunas["vacuna"] == v]["obligatoria"].iloc[0] else "(Sugerida)"
                st.markdown(f"- {v} {tipo}")
        else:
            st.info("No hay vacunas programadas para el próximo año.")


    if pendientes:
        enviar_recordatorio_vacunas(
            st.session_state.nombre_usuario,
            st.session_state.correo_usuario,
            pendientes
        )

