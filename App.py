import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="LegalGuard_Apg - SENIAT Guanta",
    page_icon="⚖",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #0b2545 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #0b2545;
        color: #ffffff;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    .stButton>button {
        background-color: #0b2545;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #134074;
        color: white;
    }
    div.stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    div.stTabs [data-baseweb="tab"] {
        background-color: #e2e8f0;
        border-radius: 4px 4px 0px 0px;
        color: #0b2545;
        font-weight: 600;
    }
    div.stTabs [aria-selected="true"] {
        background-color: #0b2545 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

ARCHIVO_PLANILLAS = "db_planillas.csv"
ARCHIVO_NOTIFICACIONES = "db_notificaciones.csv"
ARCHIVO_PODERES = "db_poderes_v9.csv"
ARCHIVO_CARTAS_PODERES = "db_cartas_poderes.csv"
ARCHIVO_FIANZAS = "db_fianzas_v9.csv"
ARCHIVO_RECUPERACION = "db_recuperacion_claves.csv"

def inicializar_archivos_locales():
    if not os.path.exists(ARCHIVO_PLANILLAS):
        pd.DataFrame(columns=["nro_control", "rif_contribuyente", "nombre_contribuyente", "tipo_tramite", "observacion_legal", "abogado_emisor", "fecha_emision"]).to_csv(ARCHIVO_PLANILLAS, index=False)
    if not os.path.exists(ARCHIVO_NOTIFICACIONES):
        pd.DataFrame(columns=["rif", "mensaje", "fecha_creacion"]).to_csv(ARCHIVO_NOTIFICACIONES, index=False)
    if not os.path.exists(ARCHIVO_RECUPERACION):
        pd.DataFrame(columns=["nombre_solicitante", "rol", "motivo", "fecha_solicitud", "estatus"]).to_csv(ARCHIVO_RECUPERACION, index=False)
    
    if not os.path.exists(ARCHIVO_PODERES):
        pd.DataFrame(columns=[
            "Correlativo", "Agencia", "RIF_del_Consignatario", 
            "Nombre_del_Consignatario", "Fecha_de_llegada", "Fecha_de_aceptacion", 
            "Fecha_de_Notificacion", "Estatus"
        ]).to_csv(ARCHIVO_PODERES, index=False)

    if not os.path.exists(ARCHIVO_CARTAS_PODERES):
        pd.DataFrame(columns=[
            "Correlativo", "Agencia", "RIF_del_Consignatario", 
            "Nombre_del_Consignatario", "BL", "Factura", "Buque", 
            "Mercancia", "Origen", "Destino", "Fecha_de_llegada", 
            "Fecha_de_aceptacion", "Fecha_de_Notificacion", "Estatus"
        ]).to_csv(ARCHIVO_CARTAS_PODERES, index=False)
        
    if not os.path.exists(ARCHIVO_FIANZAS):
        pd.DataFrame(columns=[
            "Correlativo", "Agencia", "Rif_de_la_agencia", 
            "Consignatario_si_aplica", "Rif_del_consignatario", "Contrato_de_Fianza", 
            "Anexos", "Monto", "Tipo_de_Fianza", 
            "Fecha_de_llegada", "Fecha_de_aceptacion", "Fecha_de_Notificacion", "Estatus"
        ]).to_csv(ARCHIVO_FIANZAS, index=False)

inicializar_archivos_locales()

def cargar_datos(archivo):
    try:
        return pd.read_csv(archivo)
    except:
        return pd.DataFrame()

def guardar_dataframe(df, archivo):
    df.to_csv(archivo, index=False)

def obtener_total_registros():
    return len(cargar_datos(ARCHIVO_PLANILLAS)) + len(cargar_datos(ARCHIVO_PODERES)) + len(cargar_datos(ARCHIVO_CARTAS_PODERES)) + len(cargar_datos(ARCHIVO_FIANZAS))

st.title("⚖️ LegalGuard_Apg")
st.subheader("SENIAT - Aduana Principal de Guanta | Área de Apoyo Jurídico")
st.markdown("---")

st.sidebar.header("Control de Acceso Institucional")
rol_usuario = st.sidebar.selectbox(
    "Seleccione su Rol:",
    ["Administrador (Abogado / Total)", "Administrador (Asistente Administrativo)", "Visualizador Legal", "Consignatario (Contribuyente)"]
)

clave_ingresada = st.sidebar.text_input("Contraseña de Acceso:", type="password")
acceso_concedido = False

if rol_usuario == "Administrador (Abogado / Total)" and clave_ingresada == "admin123":
    acceso_concedido = True
elif rol_usuario == "Administrador (Asistente Administrativo)" and clave_ingresada == "asistente123":
    acceso_concedido = True
elif rol_usuario == "Visualizador Legal" and clave_ingresada == "legal":
    acceso_concedido = True
elif rol_usuario == "Consignatario (Contribuyente)" and clave_ingresada == "aduana":
    acceso_concedido = True
elif clave_ingresada != "":
    st.sidebar.error("Contraseña incorrecta.")

if not acceso_concedido:
    st.warning("🔒 Por favor, seleccione su rol e ingrese la contraseña correspondiente en la barra lateral.")
    st.info("💡 **Claves de acceso:**\n- Visualizador Legal: `legal`\n- Consignatario: `aduana`")
else:
    st.sidebar.success(f"Sesión iniciada como: {rol_usuario}")
    st.sidebar.metric(label="📊 Registros Totales en Sistema", value=obtener_total_registros())

    if rol_usuario == "Administrador (Abogado / Total)":
        pestanas = st.tabs([
            "📂 Gestión de Poderes", 
            "📜 Cartas Poderes (Conteo y Gestión)", 
            "🛡 Gestión de Fianzas"
        ])
        
        with pestanas[0]:
            st.header("Consulta General de Poderes")
            df = cargar_datos(ARCHIVO_PODERES)
            st.dataframe(df, use_container_width=True)

        with pestanas[1]:
            st.header("Gestión y Análisis de Cartas Poderes")
            df_cp = cargar_datos(ARCHIVO_CARTAS_PODERES)
            
            sub_opcion = st.radio("Seleccione acción:", ["📊 Análisis y Conteo Mensual", "➕ Registrar Nueva Carta Poder"], horizontal=True)
            
            if sub_opcion == "📊 Análisis y Conteo Mensual":
                if not df_cp.empty:
                    df_cp['Fecha_de_llegada'] = pd.to_datetime(df_cp['Fecha_de_llegada'], errors='coerce')
                    df_cp['Año_Mes'] = df_cp['Fecha_de_llegada'].dt.strftime('%Y-%m')
                    
                    st.markdown("### 🔍 Filtros Analíticos con Conteo Mensual")
                    meses_disponibles = sorted(df_cp['Año_Mes'].dropna().unique(), reverse=True)
                    
                    if meses_disponibles:
                        mes_seleccionado = st.selectbox("📅 Seleccione Periodo Mensual para Análisis:", meses_disponibles)
                        df_mes = df_cp[df_cp['Año_Mes'] == mes_seleccionado]
                    else:
                        df_mes = df_cp

                    f_col1, f_col2, f_col3 = st.columns(3)
                    with f_col1:
                        st.markdown("**1. Por Agente de Aduanas**")
                        if not df_mes.empty and 'Agencia' in df_mes.columns:
                            agencias_mes = df_mes['Agencia'].unique()
                            if len(agencias_mes) > 0:
                                agencia_sel = st.selectbox("Seleccione Agencia:", agencias_mes, key="cp_ag")
                                df_ag_f = df_mes[df_mes['Agencia'] == agencia_sel]
                                st.metric(f"Conteo en {mes_seleccionado}", len(df_ag_f))
                    with f_col2:
                        st.markdown("**2. Por Consignatario**")
                        if not df_mes.empty and 'Nombre_del_Consignatario' in df_mes.columns:
                            cons_mes = df_mes['Nombre_del_Consignatario'].unique()
                            if len(cons_mes) > 0:
                                consignatario_sel = st.selectbox("Seleccione Consignatario:", cons_mes, key="cp_co")
                                df_co_f = df_mes[df_mes['Nombre_del_Consignatario'] == consignatario_sel]
                                st.metric(f"Conteo Mensual", len(df_co_f))
                    with f_col3:
                        st.markdown("**3. Buques Diferentes**")
                        if not df_mes.empty:
                            df_mb = df_mes.groupby('Nombre_del_Consignatario')['Buque'].nunique().reset_index()
                            df_mb.columns = ['Consignatario', 'Buques Diferentes (Mes)']
                            st.dataframe(df_mb, use_container_width=True)
                    st.markdown("---")
                
                st.dataframe(df_cp, use_container_width=True)
                
            elif sub_opcion == "➕ Registrar Nueva Carta Poder":
                st.subheader("Formulario de Registro - Carta Poder")
                with st.form("form_carta_poder"):
                    col1, col2 = st.columns(2)
                    with col1:
                        correlativo = st.text_input("Correlativo")
                        agencia = st.text_input("Agencia de Aduanas")
                        rif_cons = st.text_input("RIF del Consignatario")
                        nombre_cons = st.text_input("Nombre del Consignatario")
                        bl = st.text_input("B/L (Bill of Lading)")
                        factura = st.text_input("Factura")
                    with col2:
                        buque = st.text_input("Buque")
                        mercancia = st.text_input("Mercancía")
                        origen = st.text_input("Origen")
                        destino = st.text_input("Destino")
                        fecha_llegada = st.date_input("Fecha de Llegada", value=datetime.today())
                        estatus = st.selectbox("Estatus", ["Pendiente", "Aprobado", "Observado"])
                    
                    btn_guardar = st.form_submit_button("Guardar Carta Poder")
                    if btn_guardar:
                        nuevo_reg = {
                            "Correlativo": correlativo, "Agencia": agencia, "RIF_del_Consignatario": rif_cons,
                            "Nombre_del_Consignatario": nombre_cons, "BL": bl, "Factura": factura, "Buque": buque,
                            "Mercancia": mercancia, "Origen": origen, "Destino": destino,
                            "Fecha_de_llegada": str(fecha_llegada), "Fecha_de_aceptacion": "", "Fecha_de_Notificacion": "", "Estatus": estatus
                        }
                        df_cp = pd.concat([df_cp, pd.DataFrame([nuevo_reg])], ignore_index=True)
                        guardar_dataframe(df_cp, ARCHIVO_CARTAS_PODERES)
                        st.success("¡Carta Poder registrada con éxito!")

        with pestanas[2]:
            st.header("Consulta General de Fianzas")
            df = cargar_datos(ARCHIVO_FIANZAS)
            st.dataframe(df, use_container_width=True)
            
    elif rol_usuario == "Visualizador Legal":
        st.header("Módulo de Consulta - Cartas Poderes")
        df_cp = cargar_datos(ARCHIVO_CARTAS_PODERES)
        st.dataframe(df_cp, use_container_width=True)
    else:
        st.info("Seleccione un rol autorizado para ver los módulos.")
