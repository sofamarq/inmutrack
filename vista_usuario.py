import streamlit as st
from historial_usuario import mostrar_historial_usuario
from vacunas_pendientes import mostrar_vacunas_pendientes
from PIL import Image
import base64
from io import BytesIO
from datetime import datetime
import pandas as pd
from funciones_supabase import actualizar_usuario
from funciones_supabase import obtener_historial_vacunacion_usuario, transformar_vacunas_dataframe


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
        st.markdown("Te damos la bienvenida a tu panel personal de Inmutrack.")

        dni = st.session_state.get("dni", "")
        usuario = st.session_state.get("usuario_actual", {})

        fecha_nacimiento = usuario.get("fecha_nacimiento", "")
        if not fecha_nacimiento:
            st.warning("No se encontró la fecha de nacimiento.")
            return

        edad_actual_meses = (datetime.today() - datetime.strptime(fecha_nacimiento, "%Y-%m-%d")).days // 30

        resultado = obtener_historial_vacunacion_usuario(int(dni))
        historial = resultado.data if resultado and resultado.data else []

        cantidad_dosis = len(historial)

        vacunas_df = transformar_vacunas_dataframe().drop_duplicates(subset=["nombre_vacuna"])

        aplicadas = {r["vacunas"]["nombre_vacuna"] for r in historial if r.get("vacunas")}

        pendientes = []
        proximas = []

        for _, row in vacunas_df.iterrows():
            if row["edad_1ra_dosis"] is None:
                continue

            nombre = row["nombre_vacuna"]
            edad_1ra = row["edad_1ra_dosis"]
            refuerzo = row["refuerzo"]

            if edad_1ra <= edad_actual_meses and nombre not in aplicadas:
                pendientes.append(nombre)
            elif nombre not in aplicadas:
                if edad_1ra > edad_actual_meses:
                    proximas.append(nombre)
                elif refuerzo and (edad_1ra + refuerzo) > edad_actual_meses:
                    proximas.append(nombre)

        # Visualización
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💉 Vacunas pendientes")
            if pendientes:
                st.warning(f"🔔 Tenés {len(set(pendientes))} vacunas pendientes por aplicar")
            else:
                st.success("✔️ No tenés vacunas pendientes.")
        with col2:
            st.subheader("📋 Dosis aplicadas")
            st.success(f"{cantidad_dosis} dosis registradas")

    elif opcion == "Mis datos":
        st.header("🪪 Mis datos personales")

        usuario = st.session_state.get("usuario_actual", {})
        st.session_state["dni"] = usuario.get("user_id", "")

        datos_usuario = {
            "Nombre": usuario.get("nombre", ""),
            "Apellido": usuario.get("apellido", ""),
            "DNI": usuario.get("user_id", ""),
            "Fecha de nacimiento": usuario.get("fecha_nacimiento", "")
        }

        for campo, valor in datos_usuario.items():
            st.markdown(f"**{campo}:** {valor}")

        st.markdown("---")

        # --- Datos editables ---
        with st.form("form_mis_datos"):
            localidad = st.text_input("Localidad", value=usuario.get("localidad", ""))
            telefono = st.text_input("Teléfono de contacto", value=usuario.get("telefono_contacto", ""))
            email = st.text_input("Correo electrónico", value=usuario.get("correo_electronico", ""))
            personal_salud = st.checkbox("¿Es personal de salud?", value=usuario.get("personal_salud", False))
            embarazada = st.checkbox("¿Está embarazada?", value=usuario.get("embarazada", False))

            if st.form_submit_button("Guardar cambios"):
                cambios = {
                    "user_id": usuario.get("user_id"),
                    "localidad": localidad,
                    "telefono_contacto": telefono,
                    "correo_electronico": email,
                    "personal_salud": personal_salud,
                    "embarazada": embarazada
                }

                resultado = actualizar_usuario(cambios)

                if "error" in resultado and resultado["error"]:
                    st.error("❌ No se pudo guardar el cambio.")
                    st.text(resultado["error"]["message"])
                else:
                    st.session_state.usuario_actual.update(cambios)
                    st.success("✅ Cambios guardados correctamente.")

    elif opcion == "Historial de vacunación":
        mostrar_historial_usuario()

    elif opcion == "Vacunas pendientes/próximas":
        mostrar_vacunas_pendientes()

    elif opcion == "Cerrar sesión":
        st.session_state.rol = None
        st.session_state.pagina_actual = "inicio"
        st.rerun()
