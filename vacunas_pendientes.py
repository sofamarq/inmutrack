import streamlit as st
import pandas as pd
from datetime import datetime
from envio_mail import enviar_recordatorio_vacunas
from funciones_supabase import obtener_datos_usuario_y_historial, transformar_vacunas_dataframe

# --- Lógica principal ---
def mostrar_vacunas_pendientes():
    st.header("🧾 Vacunas pendientes")

    dni = st.session_state.get("dni")
    if not dni:
        st.warning("No se encontró el DNI del usuario en sesión.")
        return

    usuario, historial = obtener_datos_usuario_y_historial(dni)
    vacunas = transformar_vacunas_dataframe()
    vacunas = vacunas.drop_duplicates(subset=["nombre_vacuna"])

    edad_hoy = (datetime.today() - datetime.strptime(usuario["fecha_nacimiento"], "%Y-%m-%d")).days // 30  # en meses
    edad_proximo_anio = edad_hoy + 12

    aplicadas = [v["vacuna"] for v in historial]
    pendientes = []
    proximas = []
    completadas = []

    # Determinar "obligatoria ajustada" por cada vacuna
    vacunas["obligatoria_ajustada"] = vacunas.apply(
        lambda row: row["obligatoria"]
        or (row.get("embarazada", False) and usuario.get("embarazada", False))
        or (row.get("personalsalud", False) and usuario.get("personal_salud", False)),
        axis=1
    )

    for _, row in vacunas.iterrows():
        nombre_vac = row["nombre_vacuna"]
        recibidas = [v for v in historial if v["vacuna"] == nombre_vac]

        if row["edad_1ra_dosis"] <= edad_hoy:
            if not recibidas:
                pendientes.append(nombre_vac)
            else:
                completadas.append(nombre_vac)

        if row["refuerzo"] and row["edad_1ra_dosis"] <= edad_proximo_anio < row["edad_1ra_dosis"] + row["refuerzo"]:
            proximas.append(nombre_vac)

    # Filtro por tipo de vacuna
    filtro_tipo = st.selectbox("Filtrar por tipo de vacuna", ["Todas", "Obligatoria", "Sugerida"])

    # Mostrar tabla resumen
    st.subheader("📊 Resumen de estado de vacunación")
    df_estado = pd.DataFrame([
        {
            "Vacuna": v,
            "Estado": ("Pendiente" if v in pendientes else ("Próxima" if v in proximas else "Aplicada")),
            "Tipo": ("Obligatoria" if vacunas[vacunas["nombre_vacuna"] == v]["obligatoria_ajustada"].iloc[0] else "Sugerida")
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
                tipo = "(Obligatoria)" if vacunas[vacunas["nombre_vacuna"] == v]["obligatoria_ajustada"].iloc[0] else "(Sugerida)"
                st.markdown(f"- {v} {tipo}")
        else:
            st.success("No hay vacunas pendientes 🎉")

    with col2:
        st.subheader("📅 Próximas vacunas")
        if proximas:
            for v in proximas:
                tipo = "(Obligatoria)" if vacunas[vacunas["nombre_vacuna"] == v]["obligatoria_ajustada"].iloc[0] else "(Sugerida)"
                st.markdown(f"- {v} {tipo}")
        else:
            st.info("No hay vacunas programadas para el próximo año.")

    if pendientes:
        enviar_recordatorio_vacunas(
            st.session_state.nombre_usuario,
            st.session_state.correo_usuario,
            pendientes
        )

