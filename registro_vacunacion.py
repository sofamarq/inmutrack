#lo unico es que despues de cargar un registro no se limpian los campos, y tampoco logro redirigirlo a la pagina inicial del centro

import streamlit as st
from datetime import date
import time
from funciones_supabase import registrar_aplicacion, obtener_vacunas

def mostrar_registro_vacuna():
    st.header("💉 Registro de aplicación de vacuna")

    # Simulación de datos de vacunas (como si vinieran de Supabase)
    # vacunas_disponibles = {
    #     101: "COVID-19",
    #     102: "Triple Viral",
    #     103: "BCG",
    #     104: "Antigripal",
    #     105: "Hepatitis B"
    # }

    vacunas_response = obtener_vacunas()
    vacunas_disponibles = {}

    if vacunas_response.data:
        # Mapeo: nombre -> id
        vacunas_disponibles = {
            v["id_vacuna"]: v["nombre_vacuna"]
            for v in vacunas_response.data
            if "id_vacuna" in v and "nombre_vacuna" in v
        }
    else:
        st.error("❌ No se pudieron cargar las vacunas desde la base de datos.")

    paciente_dni = st.text_input("DNI del paciente")
    vacuna_id = st.selectbox("Código de vacuna", list(vacunas_disponibles.keys()), key="vacuna_select")
    vacuna_nombre = vacunas_disponibles.get(vacuna_id, "")
    st.markdown(f"**Nombre de la vacuna:** {vacuna_nombre}")

    with st.form("form_vacuna"):
        fecha_aplicacion = st.date_input("Fecha de aplicación", max_value=date.today())
        lote = st.text_input("Número de lote")

        # Centro desde sesión
        centro = st.session_state.get("nombre_centro", "[Centro no identificado]")
        st.markdown(f"**Centro responsable:** {centro}")

        confirmacion = st.checkbox("Confirmo que los datos ingresados son correctos", value=False)

        submit = st.form_submit_button("Registrar vacuna")

    # if submit:
    #     if not all([paciente_dni, vacuna_id, fecha_aplicacion, lote]) or not confirmacion:
    #         st.warning("⚠️ Por favor, completá todos los campos y confirmá que los datos son correctos.")
    #     else:
    #         # Simulación de guardado exitoso
    #         st.success("✅ Vacuna registrada correctamente.")
    #         st.info(f"Paciente: {paciente_dni} | Vacuna: {vacuna_nombre} (ID: {vacuna_id}) | Fecha: {fecha_aplicacion} | Lote: {lote} | Centro: {centro}")
#------------------------------------          
            #st.info("Redirigiendo al inicio...")
            #time.sleep(5)
            #st.session_state.pagina_actual = "centro_inicio"
            #st.rerun()

            ##no funcionó
#-------------------------------
    
    if submit:
        centro_id = st.session_state.get("id_centro")
        centro_nombre = st.session_state.get("nombre_centro", "[Centro no identificado]")
        if not all([paciente_dni, vacuna_id, fecha_aplicacion, lote, centro_id]) or not confirmacion:
            st.warning("⚠️ Completá todos los campos y confirmá que los datos son correctos.")
        else:
            data = {
                "id_usuario": int(paciente_dni),
                "id_centro": centro_id,
                "id_vacuna": vacuna_id,
                "fecha_aplicacion": str(fecha_aplicacion),
                "numero_lote": lote
            }

            result = registrar_aplicacion(data)

            if "error" in result and result["error"]:
                st.error("❌ Error al registrar la vacuna.")
                st.text(result["error"]["message"])
            else:
                st.success("✅ Vacuna registrada correctamente.")
                st.info(f"Paciente: {paciente_dni} | Vacuna: {vacuna_nombre} | Fecha: {fecha_aplicacion} | Lote: {lote} | Centro: {centro_nombre}")