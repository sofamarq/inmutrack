import streamlit as st
from historial_usuario import mostrar_historial_usuario
from vacunas_pendientes import mostrar_vacunas_pendientes
from PIL import Image
import base64
from io import BytesIO

def mostrar_vista_usuario():
    with st.sidebar:
        st.markdown("## 👤 Usuario")
        st.markdown(f"**{st.session_state.nombre_usuario}**")
        opcion = st.radio("Navegación", ["Inicio", "Mis datos", "Historial de vacunación", "Vacunas pendientes/próximas", "Cerrar sesión"], index=0)

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
        st.header(f"👋 ¡Bienvenida, {st.session_state.nombre_usuario}!")
        st.markdown("Te damos la bienvenida a tu panel personal de Inmutrack. Desde aquí podrás:")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💉 Próxima vacuna")
            st.info("Triple Viral - 12/05/2025")
        with col2:
            st.subheader("📋 Dosis aplicadas")
            st.success("7 dosis registradas")

        st.markdown("---")
        st.markdown("""
        - 📇 **Mis datos**: revisá y actualizá tu información personal  
        - 📋 **Historial**: consultá qué vacunas te fueron aplicadas  
        - 🧾 **Pendientes**: enterate qué dosis te falta completar  
        """)

    #elif opcion == "Mis datos":
       # st.header("📇 Mis datos personales")
      #  with st.form("form_mis_datos"):
      #      telefono = st.text_input("Teléfono de contacto", value="1122334455")
      #      email = st.text_input("Correo electrónico", value="ana@email.com")
      #      personal_salud = st.checkbox("¿Es personal de salud?", value=True)
      #      embarazada = st.checkbox("¿Está embarazada?", value=False)
      #      if st.form_submit_button("Guardar cambios"):
      #          st.success("✅ Cambios guardados correctamente.")

    elif opcion == "Mis datos":
        st.header("📇 Mis datos personales")

    # --- Datos simulados (más adelante se obtendrán de Supabase) ---
        datos_usuario = {
            "Nombre": "Ana",
            "Apellido": "Pérez",
            "DNI": "12345678",
            "Fecha de nacimiento": "2000-01-01"
         }

        for campo, valor in datos_usuario.items():
            st.markdown(f"**{campo}:** {valor}")

        st.markdown("---")

    # --- Datos editables ---
        with st.form("form_mis_datos"):
            localidad = st.text_input("Localidad", value="CABA")
            telefono = st.text_input("Teléfono de contacto", value="1122334455")
            email = st.text_input("Correo electrónico", value="ana@email.com")
            personal_salud = st.checkbox("¿Es personal de salud?", value=True)
            embarazada = st.checkbox("¿Está embarazada?", value=False)

            if st.form_submit_button("Guardar cambios"):
                # T.ODO: Actualizar en Supabase
                st.success("✅ Cambios guardados correctamente.")


    elif opcion == "Historial de vacunación":
        mostrar_historial_usuario()

    elif opcion == "Vacunas pendientes/próximas":
        mostrar_vacunas_pendientes()

    elif opcion == "Cerrar sesión":
        st.session_state.rol = None
        st.session_state.pagina_actual = "inicio"
        st.rerun()
