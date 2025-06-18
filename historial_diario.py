import streamlit as st
import pandas as pd
from datetime import date
from funciones_supabase import obtener_aplicaciones_por_fecha

def mostrar_historial_diario():
    st.header("📆 Historial diario de aplicaciones")

    # Fecha a consultar
    fecha_consulta = st.date_input("Seleccionar fecha", value=date.today(), max_value=date.today())
    fecha_str = fecha_consulta.strftime("%Y-%m-%d")

    st.markdown("---")

    # Obtener ID del centro desde sesión
    id_centro = st.session_state.get("id_centro")
    if not id_centro:
        st.warning("⚠️ No se puede consultar el historial porque no se ha identificado el centro.")
        return

    # Consultar Supabase
    resultado = obtener_aplicaciones_por_fecha(fecha_str, id_centro)

    if "error" in resultado and resultado["error"]:
        st.error("❌ Error al consultar los registros.")
        st.text(resultado["error"]["message"])
        return

    registros = obtener_aplicaciones_por_fecha(fecha_str, id_centro)

    if not registros:
        st.info(f"No hay aplicaciones registradas el {fecha_str}.")
        return

    # Convertir datos a DataFrame
    df = pd.DataFrame([
        {
            "ID vacuna": r["id_vacuna"],
            "Vacuna": r["nombre_vacuna"],
            "Laboratorio": r["laboratorio"]
        } for r in registros
    ])

    st.subheader("📊 Total de vacunas aplicadas:")
    st.success(f"{len(df)} dosis registradas el {fecha_str}")

    st.markdown("---")

    # Filtros desplegables
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
        st.dataframe(df_filtrado[["ID vacuna", "Vacuna", "Laboratorio"]], use_container_width=True)
    else:
        st.info("No se encontraron aplicaciones para la fecha seleccionada.")
