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
        st.markdown("Te damos la bienvenida a tu panel personal de Inmutrack. Desde aquí podrás:")
##ver que aca dice desde aqui podras y despues no dice nada mas
        # Obtener datos reales
        dni = st.session_state.get("dni", "")
        historial_response = obtener_historial_vacunacion_usuario(int(dni))
        vacunas_df = transformar_vacunas_dataframe()
        proximas = []

        if historial_response and historial_response.data:
            historial = historial_response.data
            cantidad_dosis = len(historial)

        # Obtener edad actual del usuario en meses
            usuario = st.session_state.get("usuario_actual", {})
            fecha_nac = usuario.get("fecha_nacimiento", "")
            edad_actual_meses = (datetime.today().date() - datetime.strptime(fecha_nac, "%Y-%m-%d").date()).days // 30

            # Obtener datos del usuario actual
            usuario = st.session_state.get("usuario_actual", {})
            dni = usuario.get("user_id")
            fecha_nacimiento = usuario.get("fecha_nacimiento")

            # Edad actual en meses
            edad_actual_meses = (datetime.today() - datetime.strptime(fecha_nacimiento, "%Y-%m-%d")).days // 30

            # Obtener historial y vacunas
            historial = obtener_historial_vacunacion_usuario(dni)
            vacunas_df = transformar_vacunas_dataframe()
            vacunas_df = vacunas_df.drop_duplicates(subset=["nombre_vacuna"])
            
            if isinstance(historial, dict) and "data" in historial:
                historial = historial["data"]
            
            # Set de vacunas ya aplicadas
            aplicadas = {r["vacuna"] for r in historial if "vacuna" in r}
            
            # Inicializo listas
            pendientes_inicio = []
            proximas = []
            
            for _, row in vacunas_df.iterrows():
                if row["edad_1ra_dosis"] is None:
                    continue
            
                if row["edad_1ra_dosis"] <= edad_actual_meses and row["nombre_vacuna"] not in aplicadas:
                    pendientes_inicio.append(row["nombre_vacuna"])
                elif row["nombre_vacuna"] not in aplicadas:
                    # Calculamos próximas dosis futuras
                    if row["edad_1ra_dosis"] > edad_actual_meses:
                        proximas.append((row["nombre_vacuna"], row["edad_1ra_dosis"]))
                    elif row["refuerzo"] is not None and (row["edad_1ra_dosis"] + row["refuerzo"]) > edad_actual_meses:
                        proximas.append((row["nombre_vacuna"], row["edad_1ra_dosis"] + row["refuerzo"]))
            
            # Visualización
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("💉 Próxima vacuna")
                if proximas:
                    vacuna_proxima = sorted(proximas, key=lambda x: x[1])[0]
                    meses_faltan = vacuna_proxima[1] - edad_actual_meses
                    fecha_aprox = datetime.today().date() + pd.DateOffset(months=meses_faltan)
                    st.info(f"{vacuna_proxima[0]} - {fecha_aprox.strftime('%d/%m/%Y')}")
                else:
                    st.success("No hay vacunas próximas registradas")
            
                if pendientes_inicio:
                    st.warning(f"🔔 Tenés {len(set(pendientes_inicio))} vacunas pendientes por aplicar")
                else:
                    st.success("✔️ No tenés vacunas pendientes.")
                        with col2:
                            st.subheader("📋 Dosis aplicadas")
                            st.success(f"{cantidad_dosis} dosis registradas")
#---------
       # else:
           # with col1:
               # st.subheader("💉 Próxima vacuna")
               # st.warning("No se pudo obtener la información.")
           # with col2:
               # st.subheader("📋 Dosis aplicadas")
               # st.warning("No se pudo obtener el historial.")
#------------- esta seccion que viene abajo corre, pero se ve vacio.        
                # aplicadas = {
                #     r[0]["nombre_vacuna"]
                #     for r in historial
                #     if isinstance(r, tuple) and len(r) > 0 and isinstance(r[0], dict) and "nombre_vacuna" in r[0]
                # }

                # # Pendientes
                # pendientes_inicio = []
                # for _, row in vacunas_df.iterrows():
                #     if (
                #         row["edad_1ra_dosis"] is not None
                #         and row["edad_1ra_dosis"] <= edad_actual_meses
                #         and row["nombre_vacuna"] not in aplicadas
                #     ):
                #         pendientes_inicio.append(row["nombre_vacuna"])

                # # Próximas vacunas
                # proximas = []
                # for _, row in vacunas_df.iterrows():
                #     if (
                #         row["nombre_vacuna"] not in aplicadas
                #         and row["edad_1ra_dosis"] is not None
                #         and row["edad_1ra_dosis"] > edad_actual_meses
                #     ):
                #         proximas.append((row["nombre_vacuna"], row["edad_1ra_dosis"]))
                #     elif (
                #         row["refuerzo"] is not None
                #         and row["edad_1ra_dosis"] is not None
                #         and (row["edad_1ra_dosis"] + row["refuerzo"]) > edad_actual_meses
                #         and row["nombre_vacuna"] in aplicadas
                #     ):
                #         proximas.append((row["nombre_vacuna"], row["edad_1ra_dosis"] + row["refuerzo"]))

                # # Mostrar info en columnas
                # col1, col2 = st.columns(2)
                # with col1:
                #     st.subheader("💉 Próxima vacuna")
                #     if proximas:
                #         vacuna_proxima = sorted(proximas, key=lambda x: x[1])[0]
                #         meses_faltan = vacuna_proxima[1] - edad_actual_meses
                #         fecha_aprox = datetime.today().date() + pd.DateOffset(months=meses_faltan)
                #         st.info(f"{vacuna_proxima[0]} - {fecha_aprox.strftime('%d/%m/%Y')}")
                #     else:
                #         st.success("No hay vacunas próximas registradas")

                #     # Mostrar aviso si hay pendientes
                #     if pendientes_inicio:
                #         st.warning(f"🔔 Tenés {len(pendientes_inicio)} vacunas pendientes por aplicar.")
                #     else:
                #         st.success("✔️ No tenés vacunas pendientes.")

                # with col2:
                #     st.subheader("📋 Dosis aplicadas")
                #     st.success(f"{cantidad_dosis} dosis registradas")
#-------
        
        # col1, col2 = st.columns(2)
        # with col1:
        #     st.subheader("💉 Próxima vacuna")
        #     st.info("Triple Viral - 12/05/2025")
        # with col2:
        #     st.subheader("📋 Dosis aplicadas")
        #     st.success("7 dosis registradas")

        # st.markdown("---")
        # st.markdown("""
        # - 📇 **Mis datos**: revisá y actualizá tu información personal  
        # - 📋 **Historial**: consultá qué vacunas te fueron aplicadas  
        # - 🧾 **Pendientes**: enterate qué dosis te falta completar  
        # """)
#-----------

    elif opcion == "Mis datos":
        st.header("📇 Mis datos personales")

# --- Datos simulados (más adelante se obtendrán de Supabase) ---
        # datos_usuario = {
        #     "Nombre": "Ana",
        #     "Apellido": "Pérez",
        #     "DNI": "12345678",
        #     "Fecha de nacimiento": "2000-01-01"
        #  }
#----
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
            # localidad = st.text_input("Localidad", value="CABA")
            # telefono = st.text_input("Teléfono de contacto", value="1122334455")
            # email = st.text_input("Correo electrónico", value="ana@email.com")
            # personal_salud = st.checkbox("¿Es personal de salud?", value=True)
            # embarazada = st.checkbox("¿Está embarazada?", value=False)
            
            localidad = st.text_input("Localidad", value=usuario.get("localidad", ""))
            telefono = st.text_input("Teléfono de contacto", value=usuario.get("telefono_contacto", ""))
            email = st.text_input("Correo electrónico", value=usuario.get("correo_electronico", ""))
            personal_salud = st.checkbox("¿Es personal de salud?", value=usuario.get("personal_salud", False))
            embarazada = st.checkbox("¿Está embarazada?", value=usuario.get("embarazada", False))

            # if st.form_submit_button("Guardar cambios"):
            #     # T.ODO: Actualizar en Supabase
            #     st.success("✅ Cambios guardados correctamente.")
            
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
                    # Actualiza en memoria también
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
