import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_mail_gmail(destinatario, asunto, mensaje_html):
    remitente = st.secrets["EMAIL_ADDRESS"]
    password = st.secrets["EMAIL_APP_PASSWORD"]

    # Crear el mensaje
    msg = MIMEMultipart("alternative")
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    msg.attach(MIMEText(mensaje_html, 'html'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, password)
        servidor.send_message(msg)
        servidor.quit()
        st.toast("✉️ Recordatorio enviado con Gmail")
    except Exception as e:
        st.warning("No se pudo enviar el correo")
        st.text(f"Error: {e}")

# --- Ejemplo de integración ---
def enviar_recordatorio_vacunas(nombre_usuario, email_usuario, vacunas_pendientes):
    if vacunas_pendientes:
        vacunas_html = "".join(f"<li>{v}</li>" for v in vacunas_pendientes)
        mensaje_html = f"""
        <html>
            <body>
                <div style='text-align: center;'>
                    <img src='https://raw.githubusercontent.com/sofamarq/inmutrack/main/logo1.jpg' alt='Inmutrack Logo' style='width: 200px;'/>
                    <h2>Hola, {nombre_usuario}!</h2>
                </div>
                <p>Nuestro sistema detectó que tenés <strong>vacunas pendientes</strong> de aplicación.</p>
                <p>Estas son las dosis que aún no figuran aplicadas en tu historial:</p>
                <ul>
                    {vacunas_html}
                </ul>
                <p>Te recomendamos acercarte al centro de salud más cercano para completar tu esquema de vacunación.</p>
                <p>Gracias por utilizar <strong>Inmutrack</strong>.<br>Saludos,<br>Equipo Inmutrack</p>
            </body>
        </html>
        """
        enviar_mail_gmail(email_usuario, "📌 Recordatorio de vacunas pendientes - INMUTRACK", mensaje_html)
