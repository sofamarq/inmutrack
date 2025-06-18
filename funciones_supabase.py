import streamlit as st
import os
import pandas as pd
from supabase import create_client, Client
from datetime import date

# Inicializar conexión (usá tus claves reales de Supabase)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------- USUARIOS -----------
def registrar_usuario(data):
    #return supabase.table("usuarios").insert(data).execute()
        return supabase.rpc("insertar_usuario", {
            "p_user_id": data["dni"],
            "p_nombre": data["nombre"],
            "p_apellido": data["apellido"],
            "p_fecha_nacimiento": data["fecha_nacimiento"],
            "p_telefono_contacto": data["telefono_contacto"],
            "p_correo_electronico": data["correo_electronico"],
            "p_localidad": data["localidad"],
            "p_personal_salud": data["personal_salud"],
            "p_embarazada": data["embarazada"]
        }).execute()

def buscar_usuario_por_dni(user_id: int):
    return supabase.table("usuario").select("*").eq("user_id", user_id).limit(1).execute()

def actualizar_usuario(data: dict):
    return supabase.rpc("actualizar_usuario", {
        "p_user_id": data["user_id"],
        "p_localidad": data["localidad"],
        "p_telefono_contacto": data["telefono_contacto"],
        "p_correo_electronico": data["correo_electronico"],
        "p_personal_salud": data["personal_salud"],
        "p_embarazada": data["embarazada"]
    }).execute()

def obtener_datos_usuario_y_historial(dni: int):
    # Obtener los datos del usuario
    usuario_response = supabase.table("usuario").select("*").eq("user_id", dni).single().execute()
    usuario = usuario_response.data

    # Obtener el historial de vacunación
    historial_response = supabase.table("registro").select("""
        fecha_aplicacion,
        vacunas(nombre_vacuna)
    """).eq("id_usuario", dni).order("fecha_aplicacion").execute()

    historial = [
        {
            "vacuna": r["vacunas"]["nombre_vacuna"] if r.get("vacunas") else "",
            "fecha": r["fecha_aplicacion"]
        }
        for r in (historial_response.data or [])
    ]

    return usuario, historial
    
# ----------- CENTROS -----------
def registrar_centro(data:dict):
    #return supabase.table("centros").insert(data).execute() en el codigo pone data:dict
    return supabase.rpc("insertar_centro", {
        "p_nombre": data["nombre"],
        "p_direccion": data["direccion"],
        "p_localidad": data["localidad"],
        "p_telefono": data["telefono"],
        "p_correo_electronico": data["correo_electronico"],
        "p_medico_responsable": data["medico_responsable"]
    }).execute()

def buscar_centro_por_id(id_centro: int):
    return supabase.table("centro").select("*").eq("id_centro", id_centro).limit(1).execute()

def actualizar_responsable_centro(id_centro: int, nuevo_responsable: str):
    return supabase.rpc("actualizar_responsable_centro", {
        "p_id_centro": id_centro,
        "p_medico_responsable": nuevo_responsable
    }).execute()

# ----------- VACUNAS -----------
def obtener_vacunas():
    return supabase.table("vacunas").select("*").execute()



def transformar_vacunas_dataframe():
    resultado = obtener_vacunas()
    if not resultado.data:
        return pd.DataFrame()

    registros = resultado.data
    df = pd.DataFrame(registros)

    # Asegurar que todas las columnas relevantes existen, y si no, las agrega con valores por defecto
    columnas_esperadas = [
        'id_vacuna', 'nombre_vacuna', 'laboratorio', 'enfermedad_que_previene',
        'edad_1ra_dosis', 'edad_2da_dosis', 'edad_3ra_dosis',
        'refuerzo', 'frecuencia_refuerzo', 'obligatoria', 'embarazada', 'personalsalud'
    ]
    for col in columnas_esperadas:
        if col not in df.columns:
            df[col] = None

    return df

#def obtener_vacuna_por_id(id_vacuna):
    #return supabase.table("vacunas").select("*").eq("id_vacuna", id_vacuna).single().execute()



# ----------- APLICACIONES -----------
def registrar_aplicacion(data:dict):
    return supabase.rpc("registrar_aplicacion",{
        "p_id_usuario": data["id_usuario"],
        "p_id_centro": data["id_centro"],
        "p_id_vacuna": data["id_vacuna"],
        "p_fecha_aplicacion": data["fecha_aplicacion"],
        "p_numero_lote": data["numero_lote"]
    }).execute()

#def obtener_aplicaciones_por_dni(dni):
    #return supabase.table("aplicaciones").select("*").eq("dni", dni).execute()

def obtener_historial_vacunacion_usuario(dni: int):
    # Obtener aplicaciones
    aplicaciones = supabase.table("registro").select("*").eq("id_usuario", dni).execute()
    if not aplicaciones.data:
        return []

    # Obtener info de vacunas para hacer el merge manual
    vacunas_info = supabase.table("vacunas").select("*").execute()
    mapa_vacunas = {v["id_vacuna"]: v for v in vacunas_info.data}

    # Enriquecer registros con info de vacunas
    historial = []
    for r in aplicaciones.data:
        vacuna = mapa_vacunas.get(r["id_vacuna"], {})
        historial.append({
            "vacuna": vacuna.get("nombre_vacuna", "Desconocida"),
            "laboratorio": vacuna.get("laboratorio", ""),
            "enfermedad": vacuna.get("enfermedad_que_previene", ""),
            "fecha": r["fecha_aplicacion"]
        })

    return historial

def obtener_aplicaciones_por_fecha(fecha: str, id_centro: int):
    #return supabase.table("aplicaciones").select("*").eq("fecha", fecha).execute()
    return supabase.table("registro").select("""
        id_vacuna,
        fecha_aplicacion,
        numero_lote,
        vacunas(nombre_vacuna, laboratorio)
    """).eq("fecha_aplicacion", fecha).eq("id_centro", id_centro).execute()


def obtener_aplicaciones_por_mes(anio: int, mes: int, id_centro: int):
    mes_str = f"{anio}-{mes:02d}"
    fecha_inicio = date(anio, mes, 1)
    if mes == 12:
        fecha_fin = date(anio + 1, 1, 1)
    else:
        fecha_fin = date(anio, mes + 1, 1)

    return supabase.table("registro").select("""
        id_vacuna,
        fecha_aplicacion,
        vacuna:vacunas (
            nombre_vacuna,
            laboratorio
        )
    """).gte("fecha_aplicacion", fecha_inicio.isoformat()) \
      .lt("fecha_aplicacion", fecha_fin.isoformat()) \
      .eq("id_centro", id_centro).execute()
    
   
#def obtener_aplicaciones_por_anio(anio):
    #return supabase.table("aplicaciones").select("*").like("fecha", f"{anio}-%").execute()

def obtener_aplicaciones_anuales(anio, id_centro):
    fecha_inicio = date(anio, 1, 1)
    fecha_fin = date(anio, 12, 31)
    return supabase.table("registro").select("""
        fecha_aplicacion,
        vacunas(nombre_vacuna, laboratorio)
    """).gte("fecha_aplicacion", fecha_inicio).lte("fecha_aplicacion", fecha_fin).eq("id_centro", id_centro).execute()

