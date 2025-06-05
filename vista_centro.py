import streamlit as st
from registro_vacunacion import mostrar_registro_vacuna
from historial_diario import mostrar_historial_diario
from historial_mensual import mostrar_historial_mensual
from analisis_anual import mostrar_analisis_anual
from PIL import Image
import base64
from io import BytesIO
from funciones_supabase import actualizar_responsable_centro, obtener_aplicaciones_por_fecha, obtener_aplicaciones_por_mes

#st.session_state["id_centro"] = centro["id_centro"]

def mostrar_vista_centro():
    with st.sidebar:
        st.markdown("## 🏥 Centro de Vacunación")
        st.markdown(f"**{st.session_state.nombre_centro}**")
        opcion = st.radio("Navegación", [
            "Inicio",
            "Datos de la institución",
            "Registrar vacuna",
            "Historial diario",
            "Historial mensual",
            "Analisis anual",
            "Cerrar sesión"
        ], index=0)

        # Mostrar logo en la parte inferior de la barra lateral
        st.markdown("<hr>", unsafe_allow_html=True)
        logo = Image.open("logo1.jpg")
        buffered = BytesIO()
        logo.save(buffered, format="JPEG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()
        st.markdown(
            f"""
            <div style='text-align: center; margin-top: 20px;'>
                <img src='data:image/jpeg;base64,{img_b64}' style='width: 160px; border-radius: 12px;'/>
            </div>
            """,
            unsafe_allow_html=True
        )

    if opcion == "Inicio":
        st.header(f"👋 ¡Bienvenido, {st.session_state.nombre_centro}!")
        st.markdown("Gracias por formar parte de Inmutrack. Desde este panel podrás gestionar el proceso de vacunación en tu centro:")

        # col1, col2 = st.columns(2)
        # with col1:
        #     st.subheader("📅 Aplicaciones hoy")
        #     st.info("15 registradas")
        # with col2:
        #     st.subheader("🧑‍⚕️ Aplicaciones este mes")
        #     st.success("87 dosis aplicadas")

        from datetime import date

        id_centro = st.session_state.get("id_centro", None)
        hoy = date.today()
        anio = hoy.year
        mes = hoy.month

        aplicaciones_hoy = obtener_aplicaciones_por_fecha(hoy.isoformat(), id_centro)
        aplicaciones_mes = obtener_aplicaciones_por_mes(anio, mes, id_centro)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📅 Aplicaciones hoy")
            if aplicaciones_hoy and aplicaciones_hoy.data:
                st.info(f"{len(aplicaciones_hoy.data)} registradas")
            else:
                st.info("0 registradas")

        with col2:
            st.subheader("🧑‍⚕️ Aplicaciones este mes")
            if aplicaciones_mes and aplicaciones_mes.data:
                st.success(f"{len(aplicaciones_mes.data)} dosis aplicadas")
            else:
                st.success("0 dosis aplicadas")
#----
        st.markdown("---")
        st.markdown("""
        - 💉 **Registrar vacuna**: ingresá nuevas aplicaciones  
        - 📆 **Historial diario**: revisá las aplicaciones de hoy  
        - 🗓️ **Historial mensual**: visualizá todas las del mes  
        """)

    elif opcion == "Datos de la institución":
        st.header("🏥 Datos de la institución")

        centro = st.session_state.get("centro_actual", {})
        st.session_state["id_centro"] = centro.get("id_centro")
        datos_centro = {
            "Nombre": centro.get("nombre", ""),
            "Dirección": centro.get("direccion", ""),
            "Localidad": centro.get("localidad", ""),
            "Teléfono de contacto": centro.get("telefono", ""),
            "Correo Electrónico": centro.get("correo_electronico", "")
        }
        # datos_centro = {
        #     "Nombre": "Centro de Salud Nº1",
        #     "Dirección": "Av. San Martín 1234",
        #     "Localidad": "Buenos Aires",
        #     "Teléfono de contacto": "011-4321-1234",
        #     "Correo Electrónico": "centro@inmutrack.com"
        #  }

        for campo, valor in datos_centro.items():
            st.markdown(f"**{campo}:** {valor}")

        st.markdown("---")

        with st.form("form_responsable"):
            #responsable = st.text_input("Responsable médico a cargo", value="Dra. Ana Pérez")
            responsable = st.text_input("Responsable médico a cargo", value=centro.get("medico_responsable", ""))

            # if st.form_submit_button("Guardar cambios"):
            #     st.success("✅ Cambios guardados correctamente.")

            if st.form_submit_button("Guardar cambios"):
                resultado = actualizar_responsable_centro(centro.get("id_centro"), responsable)

                if "error" in resultado and resultado["error"]:
                    st.error("❌ No se pudo guardar el cambio.")
                    st.text(resultado["error"]["message"])
                else:
                    # Actualizá también en sesión
                    st.session_state.centro_actual["medico_responsable"] = responsable
                    st.success("✅ Cambios guardados correctamente.")  

    elif opcion == "Registrar vacuna":
        mostrar_registro_vacuna()

    elif opcion == "Historial diario":
        mostrar_historial_diario()

    elif opcion == "Historial mensual":
        mostrar_historial_mensual()

    elif opcion == "Analisis anual":
        mostrar_analisis_anual()

    elif opcion == "Cerrar sesión":
        st.session_state.rol = None
        st.session_state.pagina_actual = "inicio"
        st.rerun()
