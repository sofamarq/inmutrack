#Impecable

import streamlit as st
import time
from PIL import Image
import base64
from io import BytesIO
from vista_usuario import mostrar_vista_usuario
from vista_centro import mostrar_vista_centro
from registro_usuario import mostrar_registro_usuario
from registro_centro import mostrar_registro_centro

st.set_page_config(page_title="INMUTRACK")

# Inicializar el estado si no existe
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "inicio"
if "rol" not in st.session_state:
    st.session_state.rol = None
if "nombre_usuario" not in st.session_state:
    st.session_state.nombre_usuario = ""

# Función para mostrar el logo con estilo
def mostrar_logo():
    st.markdown("""
        <style>
        .stApp {
            background-color: #f0f8ff;  /* azul muy clarito */
        }
        .description {
            text-align: center;
            font-size: 18px;
            margin-top: 10px;
            margin-bottom: 30px;
            color: #333;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .logo-img {
            width: 400px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    logo = Image.open("logo1.jpg")
    buffered = BytesIO()
    logo.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    st.markdown(f"""
        <div class="logo-container">
            <img class="logo-img" src="data:image/png;base64,{img_b64}">
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='description'>Consultá tu historial o registrá vacunas como centro de salud.</div>", unsafe_allow_html=True)

# Simuladores de funciones
def dni_exists(dni):
    return dni == "12345678"

def id_centro_exist(id_centro):
    return id_centro == "CENTRO123"

# Vista de inicio
if st.session_state.pagina_actual == "inicio":
    with st.sidebar:
        st.markdown("## 🧬 ¿Qué es Inmutrack?")
        st.markdown("Una plataforma para gestionar la vacunación de forma ordenada, segura y accesible.")

        st.markdown("## 🗓️ Calendario de vacunación")
        cal_img = Image.open("calendario.jpg")  # asegurate de tener esta imagen
        st.image(cal_img, caption="Calendario Nacional de Vacunación")

    mostrar_logo()

    tab1, tab2 = st.tabs(["Soy Usuario", "Soy Centro de Vacunación"])

    with tab1:
        st.header("👤 Ingreso de Usuario")
        dni = st.text_input("Ingrese su DNI")
        if dni:
            if dni_exists(dni):
                st.session_state.rol = "usuario"
                st.session_state.nombre_usuario = "Ana Pérez"  # Simulado, normalmente lo sacás de la BD
                st.session_state.correo_usuario = "sofiamarquevich@gmail.com"
                st.session_state.pagina_actual = "usuario_inicio"
                st.rerun()
            else:
                with st.spinner("DNI no registrado. Redirigiendo a registro..."):
                    time.sleep(2)
                st.session_state.pagina_actual = "registro_usuario"
                st.rerun()

    with tab2:
        st.header("🏥 Ingreso de Centro de Vacunación")
        id_centro = st.text_input("Ingrese su ID de centro")
        if id_centro:
            if id_centro_exist(id_centro):
                st.session_state.rol = "centro"
                st.session_state.nombre_centro = "Centro de Salud Nº 1"  # simulado
                st.session_state.pagina_actual = "centro_inicio"
                st.rerun()
            else:
                with st.spinner("Centro no registrado. Redirigiendo a registro..."):
                    time.sleep(2)
                st.session_state.pagina_actual = "registro_centro"
                st.rerun()

# Usuario logueado
elif st.session_state.pagina_actual == "usuario_inicio":
    mostrar_vista_usuario()
    

# Centro logueado
elif st.session_state.pagina_actual == "centro_inicio":
    mostrar_vista_centro()

   
# Otras páginas simuladas
elif st.session_state.pagina_actual == "registro_usuario":
    mostrar_registro_usuario()
    #st.header("📝 Registro de nuevo usuario")
    st.button("⬅️ Volver al inicio", on_click=lambda: st.session_state.update(pagina_actual="inicio")) #este boton podia ponerlo en registro, pero anda mejor desde aca.


elif st.session_state.pagina_actual == "registro_centro":
    mostrar_registro_centro()
    #st.header("🏥 Registro de nuevo centro de vacunación")
    st.button("⬅️ Volver al inicio", on_click=lambda: st.session_state.update(pagina_actual="inicio"))

# Footer
st.markdown("""
---
<p style='text-align: center; font-size: small;'>Aplicación desarrollada para la gestión de vacunación nacional.</p>
""", unsafe_allow_html=True)

