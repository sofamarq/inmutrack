import streamlit as st
import time
from PIL import Image
import base64
from io import BytesIO
from funciones_supabase import registrar_centro

def mostrar_registro_centro():

    # Cargar imagen del logo
    logo = Image.open("logo1.jpg")
    buffered = BytesIO()
    logo.save(buffered, format="JPEG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    # Mostrar logo centrado
    st.markdown(
        f"""
        <div style='text-align: center; margin-top: 30px;'>
        <img src='data:image/jpeg;base64,{img_b64}' style='width: 250px; border-radius: 12px;' />
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("   ")

    st.header("🏥 Registro de nuevo centro de vacunación")

    with st.form("form_registro_centro"):
        nombre = st.text_input("Nombre del centro", max_chars=100)
        direccion = st.text_input("Dirección", max_chars=150)
        localidad = st.text_input("Localidad", max_chars=100)
        telefono = st.text_input("Teléfono de contacto", max_chars=30)
        correo = st.text_input("Correo electrónico", max_chars=100)
        responsable = st.text_input("Nombre del responsable médico", max_chars=100)

        submit = st.form_submit_button("Registrar centro")

    # if submit:
    #     if not all([nombre, direccion, localidad, telefono, correo, responsable]):
    #         st.warning("⚠️ Todos los campos son obligatorios. Por favor completá la información.")
    #     else:
    #         # Aquí iría la lógica para registrar en Supabase en el futuro
    #         st.success("✅ Centro registrado correctamente.")

    #         st.info("Redirigiendo al inicio...")
    #         time.sleep(3)
    #         st.session_state.pagina_actual = "inicio"
    #         st.rerun()
    
    if submit:
        if not all([nombre, direccion, localidad, telefono, correo, responsable]): #aca decia contrasena
            st.warning("⚠️ Todos los campos son obligatorios. Por favor completá la información.")
        else:
            data = {
                "nombre": nombre,
                "direccion": direccion,
                "localidad": localidad,
                "telefono": telefono,
                "correo_electronico": correo,
                "medico_responsable": responsable,
                #"contrasena": contrasena
            }

            result = registrar_centro(data)

            if "error" in result and result["error"]:
                st.error("❌ Ocurrió un error al registrar el centro.")
                st.text(result["error"]["message"])
            else:
                st.success("✅ Centro registrado correctamente.")
                st.info("Redirigiendo al inicio...")
                time.sleep(3)
                st.session_state.pagina_actual = "inicio"
                st.rerun()

