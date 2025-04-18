import streamlit as st
from datetime import date
import time
from PIL import Image
import base64
from io import BytesIO

def mostrar_registro_usuario():

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
    st.header("📝 Registro de nuevo usuario")

    with st.form("form_registro"):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        dni = st.text_input("DNI")
        fecha_nacimiento = st.date_input("Fecha de nacimiento", min_value=date(1900, 1, 1), max_value=date.today())
        telefono = st.text_input("Teléfono")
        localidad = st.text_input("Localidad")
        #ocupacion = st.text_input("Ocupación") #este esta en el ERD pero no es relevante
        correo_electronico = st.text_input("Correo electrónico")
        personal_salud = st.checkbox("¿Es personal de salud?")
        embarazada = st.checkbox("¿Está embarazada?")

        submit = st.form_submit_button("Registrar")

    if submit:
        if not all([nombre, apellido, dni, telefono, localidad, correo_electronico]):
            st.warning("⚠️ Por favor, completá todos los campos obligatorios.")
            return
        st.success("✅ Los datos se registraron correctamente.")
       
        st.info("Redirigiendo al inicio...")
        time.sleep(3)
        st.session_state.pagina_actual = "inicio"
        st.rerun()
    
    #st.button("⬅️ Volver al inicio", on_click=lambda: st.session_state.update(pagina_actual="inicio")) #este boton podia ponerlo en registro, pero anda mejor desde aca.
