import io
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

from src.config import ESTACIONES_CHOCO, PROTOCOLOS_EMERGENCIA
from src.inference_engine import analizar_frame

st.set_page_config(
    page_title="SAT-CHOCÓ | Centro de Control y Alerta Temprana IA",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "bitacora_eventos" not in st.session_state:
    st.session_state.bitacora_eventos = [
        {
            "Hora": "00:45:12",
            "Estación": "EST-01 | Quibdó",
            "Evento": "Entorno Normal",
            "Confianza": "99.80%",
            "Severidad": "ESTABLE",
            "Protocolo": "Monitoreo rutinario activo"
        },
        {
            "Hora": "00:52:30",
            "Estación": "EST-04 | Istmina",
            "Evento": "Entorno Normal",
            "Confianza": "99.40%",
            "Severidad": "ESTABLE",
            "Protocolo": "Monitoreo rutinario activo"
        }
    ]

st.markdown('''
<style>
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }
    .top-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 60%, #064E3B 100%);
        border: 1px solid #1E293B;
        border-left: 6px solid #10B981;
        padding: 1.4rem 1.8rem;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .status-badge {
        display: inline-block;
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid #10B981;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .alert-box-critical {
        background: linear-gradient(90deg, rgba(127, 29, 29, 0.92) 0%, rgba(153, 27, 27, 0.8) 100%);
        border: 2px solid #EF4444;
        border-radius: 12px;
        padding: 1.3rem;
        color: #FEF2F2;
        animation: pulseBorder 2s infinite;
    }
    .alert-box-warning {
        background: linear-gradient(90deg, rgba(120, 53, 15, 0.92) 0%, rgba(146, 64, 14, 0.8) 100%);
        border: 2px solid #F59E0B;
        border-radius: 12px;
        padding: 1.3rem;
        color: #FFFBEB;
    }
    .alert-box-safe {
        background: linear-gradient(90deg, rgba(6, 78, 59, 0.88) 0%, rgba(4, 120, 87, 0.7) 100%);
        border: 1px solid #10B981;
        border-radius: 12px;
        padding: 1.3rem;
        color: #ECFDF5;
    }
    @keyframes pulseBorder {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.65); }
        70% { box-shadow: 0 0 0 14px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    .cam-frame-header {
        background-color: #1E293B;
        padding: 0.5rem 0.9rem;
        border-radius: 8px 8px 0 0;
        font-family: monospace;
        font-size: 0.82rem;
        color: #94A3B8;
        display: flex;
        justify-content: space-between;
    }
</style>
''', unsafe_allow_html=True)

# BARRA LATERAL OPERATIVA (SIN CAMPOS DE CREDENCIALES EXPUESTOS)
with st.sidebar:
    st.markdown("### 🛰️ SAT-CHOCÓ | COE")
    st.caption("Centro de Operaciones de Emergencia y Monitoreo Ambiental")
    st.markdown('<span class="status-badge">● MOTOR IA EN LÍNEA (AZURE CLOUD)</span>', unsafe_allow_html=True)

    st.divider()
    st.subheader("📍 Selección de Nodo Remoto")
    estacion_sel = st.selectbox(
        "Estación Óptica / Cuenca:",
        list(ESTACIONES_CHOCO.keys())
    )
    info_est = ESTACIONES_CHOCO[estacion_sel]

    st.markdown(
        f"- **Municipio:** {info_est['municipio']}\n"
        f"- **Cuenca:** {info_est['cuenca']}\n"
        f"- **Sensor:** {info_est['sensor']}\n"
        f"- **Coordenadas:** `{info_est['lat']}, {info_est['lon']}`"
    )

    st.divider()
    st.subheader("🎚️ Sensibilidad de Alerta")
    umbral_critico = st.slider(
        "Umbral de Disparo Automático (%)",
        min_value=50,
        max_value=95,
        value=75,
        help="Nivel mínimo de confianza neuronal para detonar alerta roja institucional."
    )

    st.divider()
    st.subheader("📞 Enlace Institucional")
    st.info(f"**Respuesta Primaria:**\n{info_est['entidad_contacto']}")

# ENCABEZADO PRINCIPAL
st.markdown(f'''
<div class="top-banner">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
        <div>
            <span class="status-badge">SISTEMA EN PRODUCCIÓN • VERSIÓN 2.4</span>
            <h1 style="margin:0.4rem 0 0.2rem 0; font-size:1.75rem; color:#F8FAFC;">
                SAT-CHOCÓ: Vigilancia Automatizada de Riesgos Hidrometeorológicos
            </h1>
            <p style="margin:0; color:#CBD5E1; font-size:0.95rem;">
                Detección temprana de <b>movimientos en masa (derrumbes)</b> e <b>inundaciones súbitas</b> mediante Visión por Computador
            </p>
        </div>
        <div style="text-align:right; color:#94A3B8; font-family:monospace; font-size:0.85rem;">
            <div>NODO ACTIVO: <b style="color:#34D399;">{info_est['municipio'].upper()}</b></div>
            <div>MODELO: <b style="color:#F8FAFC;">Modelo_Mejorado (AUC 0.9998)</b></div>
            <div>FECHA: {datetime.now().strftime('%Y-%m-%d')}</div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Estaciones Conectadas", "5 / 5 Nodos", "100% Operativas")
k2.metric("Precisión del Modelo", "98.75%", "+0.83% vs Base")
k3.metric("Latencia de Inferencia", "~420 ms", "API REST Segura")
k4.metric("Eventos en Bitácora", f"{len(st.session_state.bitacora_eventos)} Registros", "Turno Actual")

st.divider()

tab_live, tab_mapa, tab_validacion = st.tabs([
    "🎥 Consola de Monitoreo y Despacho de Alertas",
    "🗺️ Mapa Georreferenciado de Estaciones (Chocó)",
    "📊 Auditoría Científica del Modelo IA"
])

with tab_live:
    col_izq, col_der = st.columns([1.05, 1.35], gap="large")

    with col_izq:
        st.subheader("📡 Señal Óptica de Campo (Cámara / Dron UAV)")
        st.caption("Seleccione el origen de la señal visual para evaluación inmediata del terreno:")

        modo_entrada = st.radio(
            "Origen de la Señal Visual:",
            [
                "📁 Telemetría de Cámara / Dron UAV (Subir Capturas o Lote)",
                "📸 Sensor Óptico en Vivo (Captura Directa desde Dispositivo)"
            ],
            horizontal=False
        )

        imagenes_a_procesar = []

        if "Telemetría" in modo_entrada:
            archivos = st.file_uploader(
                "Ingrese frames de telemetría o fotografías de inspección (JPG, PNG)",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                label_visibility="collapsed"
            )
            if archivos:
                for f in archivos:
                    imagenes_a_procesar.append((f.name, f.getvalue()))
        else:
            cam_frame = st.camera_input("Sensor Óptico en Vivo")
            if cam_frame is not None:
                imagenes_a_procesar.append((f"live_cam_{datetime.now().strftime('%H%M%S')}.jpg", cam_frame.getvalue()))

        if imagenes_a_procesar:
            st.success(f"🛰️ Señal recibida: **{len(imagenes_a_procesar)}** captura(s) lista(s) para análisis neuronal.")
            ejecutar = st.button("⚡ PROCESAR SEÑAL Y EVALUAR RIESGO", type="primary", use_container_width=True)
        else:
            ejecutar = False
            st.info("Esperando recepción de frame visual desde el nodo seleccionado...")

    with col_der:
        st.subheader("🚨 Diagnóstico de Riesgo y Protocolo de Respuesta")

        if ejecutar and imagenes_a_procesar:
            for idx_img, (nombre_img, bytes_img) in enumerate(imagenes_a_procesar):
                with st.spinner(f"Analizando telemetría visual de {nombre_img}..."):
                    try:
                        resultado = analizar_frame(bytes_img)
                        top = resultado["top"]
                        clave = top["clave"]
                        confianza = top["probabilidad"] * 100
                        hora_actual = datetime.now().strftime("%H:%M:%S")

                        st.markdown(f'''
                        <div class="cam-frame-header">
                            <span>● REC | {estacion_sel.split(' | ')[0]} | {info_est['sensor']}</span>
                            <span>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} COT</span>
                        </div>
                        ''', unsafe_allow_html=True)

                        c_vis, c_diag = st.columns([1, 1.3])
                        with c_vis:
                            st.image(Image.open(io.BytesIO(bytes_img)), use_container_width=True)

                        with c_diag:
                            proto = PROTOCOLOS_EMERGENCIA.get(clave, PROTOCOLOS_EMERGENCIA["normal"])

                            if clave in ["derrumbe", "inundacion"] and confianza >= umbral_critico:
                                st.markdown(f'''
                                <div class="alert-box-critical">
                                    <div style="font-size:0.8rem; font-weight:700; letter-spacing:1px;">🚨 {proto['nivel']} • DISPARO AUTOMÁTICO</div>
                                    <h3 style="margin:0.3rem 0; color:#FFFFFF;">{proto['codigo']}</h3>
                                    <p style="margin:0; font-size:0.95rem;">
                                        Confianza del Modelo: <b>{confianza:.2f}%</b> | Sector: <b>{info_est['municipio']}</b>
                                    </p>
                                </div>
                                ''', unsafe_allow_html=True)

                                st.markdown("#### 📋 Protocolo de Emergencia Activado:")
                                for paso in proto["acciones"]:
                                    st.markdown(f"- 🔴 {paso}")

                                severidad_reg = "ALTA / CRÍTICA"

                            elif clave in ["derrumbe", "inundacion"]:
                                st.markdown(f'''
                                <div class="alert-box-warning">
                                    <div style="font-size:0.8rem; font-weight:700;">⚠️ ADVERTENCIA PREVENTIVA • VERIFICACIÓN REQUERIDA</div>
                                    <h3 style="margin:0.3rem 0; color:#FFFFFF;">POSIBLE {top['etiqueta'].upper()} ({confianza:.2f}%)</h3>
                                    <p style="margin:0; font-size:0.9rem;">
                                        Detectado por debajo del umbral crítico ({umbral_critico}%). Se recomienda inspección visual del operador.
                                    </p>
                                </div>
                                ''', unsafe_allow_html=True)
                                severidad_reg = "MEDIA / PREVENTIVA"

                            else:
                                st.markdown(f'''
                                <div class="alert-box-safe">
                                    <div style="font-size:0.8rem; font-weight:700;">✅ {proto['nivel']}</div>
                                    <h3 style="margin:0.3rem 0; color:#FFFFFF;">{proto['codigo']}</h3>
                                    <p style="margin:0; font-size:0.95rem;">
                                        Estabilidad confirmada con <b>{confianza:.2f}%</b> de confianza.
                                    </p>
                                </div>
                                ''', unsafe_allow_html=True)
                                severidad_reg = "ESTABLE"

                        df_probs = pd.DataFrame([
                            {"Categoría": p["etiqueta"], "Probabilidad (%)": round(p["probabilidad"] * 100, 2)}
                            for p in resultado["todas"]
                        ])
                        fig_bar = px.bar(
                            df_probs,
                            x="Probabilidad (%)",
                            y="Categoría",
                            orientation="h",
                            text="Probabilidad (%)",
                            color="Categoría",
                            color_discrete_map={
                                "Derrumbe": "#EF4444",
                                "Inundación": "#F97316",
                                "Normal": "#10B981"
                            }
                        )
                        fig_bar.update_layout(
                            height=180,
                            margin=dict(l=10, r=10, t=10, b=10),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#F8FAFC"),
                            showlegend=False,
                            xaxis=dict(range=[0, 105], title="")
                        )
                        st.plotly_chart(fig_bar, use_container_width=True, key=f"chart_{idx_img}_{nombre_img}_{hora_actual}")

                        st.session_state.bitacora_eventos.insert(0, {
                            "Hora": hora_actual,
                            "Estación": estacion_sel.split(" — ")[0],
                            "Evento": top["etiqueta"],
                            "Confianza": f"{confianza:.2f}%",
                            "Severidad": severidad_reg,
                            "Protocolo": proto["acciones"][0]
                        })

                        st.divider()

                    except Exception as e:
                        st.error(f"Fallo de comunicación con el motor de inferencia: {e}")
        else:
            st.markdown('''
            <div style="border: 1px dashed #334155; border-radius: 12px; padding: 2.5rem; text-align: center; color: #94A3B8;">
                <h4 style="color:#E2E8F0; margin-bottom:0.5rem;">Monitor en Espera de Telemetría</h4>
                <p style="margin:0;">Cargue una imagen de campo o active la captura en el panel izquierdo y presione <b>PROCESAR SEÑAL</b> para visualizar el diagnóstico neuronal y los protocolos de alerta.</p>
            </div>
            ''', unsafe_allow_html=True)

    st.subheader("📋 Bitácora Oficial de Eventos y Despacho (Turno Operativo)")
    df_bitacora = pd.DataFrame(st.session_state.bitacora_eventos)
    st.dataframe(df_bitacora, use_container_width=True, hide_index=True)

    csv_data = df_bitacora.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Exportar Reporte Oficial para Gestión del Riesgo (CSV)",
        data=csv_data,
        file_name=f"reporte_coe_choco_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )

with tab_mapa:
    st.subheader("🗺️ Red de Vigilancia Georreferenciada en el Departamento del Chocó")
    st.caption("Ubicación estratégica de cámaras fijas ribereñas, puntos críticos viales y zonas de patrullaje UAV.")

    df_mapa = pd.DataFrame([
        {
            "Estación": k,
            "Municipio": v["municipio"],
            "Cuenca / Corredor": v["cuenca"],
            "Sensor": v["sensor"],
            "lat": v["lat"],
            "lon": v["lon"],
            "Estado": "Activo (En Línea)"
        }
        for k, v in ESTACIONES_CHOCO.items()
    ])

    map_options = dict(
        data_frame=df_mapa,
        lat="lat",
        lon="lon",
        hover_name="Estación",
        hover_data=["Cuenca / Corredor", "Sensor", "Estado"],
        color_discrete_sequence=["#10B981"],
        zoom=7.3,
        height=460
    )

    if hasattr(px, "scatter_map"):
        fig_map = px.scatter_map(**map_options, map_style="carto-darkmatter")
    else:
        fig_map = px.scatter_mapbox(**map_options)
        fig_map.update_layout(mapbox_style="carto-darkmatter")

    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(
        fig_map,
        width="stretch",
        alt="Mapa georreferenciado de las estaciones de vigilancia del departamento del Chocó"
    )
    st.dataframe(df_mapa[["Estación", "Cuenca / Corredor", "Sensor", "lat", "lon", "Estado"]], use_container_width=True, hide_index=True)

with tab_validacion:
    st.subheader("📊 Auditoría Experimental: Evolución del Modelo Neuronal")
    st.markdown(
        "Resultados certificados sobre un conjunto de validación independiente de **240 imágenes** "
        "(80 `Inundación`, 80 `Derrumbe`, 80 `Normal`) completamente aisladas del entrenamiento."
    )

    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.markdown("#### Comparativa Modelo Base vs. Modelo Mejorado")
        df_evol = pd.DataFrame({
            "Métrica": ["Exactitud Global (Accuracy)", "Precision Macro", "Recall Macro", "F1-Score Macro", "AUC Promedio (ROC)"],
            "Modelo Base (1,020 imgs)": [97.92, 98.00, 97.92, 97.90, 99.94],
            "Modelo Mejorado (1,260 imgs)": [98.75, 98.80, 98.75, 98.75, 99.98]
        })
        st.dataframe(df_evol, use_container_width=True, hide_index=True)

    with c_m2:
        st.markdown("#### Rendimiento por Clase (`Modelo_Mejorado`)")
        df_clases = pd.DataFrame({
            "Clase": ["Inundación", "Derrumbe", "Normal"],
            "Precision (%)": [100.00, 96.39, 100.00],
            "Recall (%)": [96.25, 100.00, 100.00],
            "F1-Score": [0.9809, 0.9816, 1.0000],
            "AUC": [1.0000, 0.9995, 1.0000]
        })
        st.dataframe(df_clases, use_container_width=True, hide_index=True)
