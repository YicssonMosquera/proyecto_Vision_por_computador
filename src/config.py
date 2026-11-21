import os
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN DE PRODUCCIÓN - CONEXIÓN AZURE CUSTOM VISION (ENCAPSULADA)
# ==============================================================================
AZURE_PREDICTION_URL = os.getenv(
    "AZURE_PREDICTION_URL",
    st.secrets.get(
        "AZURE_PREDICTION_URL",
        "https://entrega4visionporcomputador.cognitiveservices.azure.com/customvision/v3.0/Prediction/83ce4e4d-5a91-41d0-8a6a-0fe6ec2e6fb7/classify/iterations/Modelo_Mejorado/image"
    )
)

AZURE_PREDICTION_KEY = os.getenv(
    "AZURE_PREDICTION_KEY",
    st.secrets.get("AZURE_PREDICTION_KEY", "")
)

# ==============================================================================
# RED DE ESTACIONES Y PUNTOS CRÍTICOS DE MONITOREO EN EL CHOCÓ
# ==============================================================================
ESTACIONES_CHOCO = {
    "EST-01 | Quibdó — Cuenca Media Río Atrato": {
        "municipio": "Quibdó",
        "cuenca": "Río Atrato",
        "lat": 5.6947,
        "lon": -76.6611,
        "sensor": "Cámara Torre Hidrometeorológica #01",
        "entidad_contacto": "UNGRD Chocó / Cuerpo de Bomberos Quibdó (Línea 119)"
    },
    "EST-02 | Tadó — Corredor Vial Pereira - Quibdó (Sector El 18)": {
        "municipio": "Tadó",
        "cuenca": "Subcuenca Río San Juan",
        "lat": 5.2660,
        "lon": -76.5647,
        "sensor": "Cámara Vigilancia Talud Vial #04",
        "entidad_contacto": "INVÍAS Territorial Chocó / Defensa Civil Tadó"
    },
    "EST-03 | Carmen de Atrato — Vía Medellín - Quibdó (Km 32)": {
        "municipio": "El Carmen de Atrato",
        "cuenca": "Alto Atrato",
        "lat": 5.8931,
        "lon": -76.1436,
        "sensor": "Domo Óptico Laderas #02",
        "entidad_contacto": "CMGRD Carmen de Atrato / Policía de Carreteras (#767)"
    },
    "EST-04 | Istmina — Confluencia Río San Juan": {
        "municipio": "Istmina",
        "cuenca": "Río San Juan",
        "lat": 5.1606,
        "lon": -76.6839,
        "sensor": "Estación Óptica Ribereña #03",
        "entidad_contacto": "CMGRD Istmina / Cruz Roja Seccional Chocó"
    },
    "EST-05 | Alto Baudó — Pie de Pató": {
        "municipio": "Alto Baudó",
        "cuenca": "Río Baudó",
        "lat": 5.5167,
        "lon": -76.9667,
        "sensor": "Dron UAV Patrullaje Autónomo #05",
        "entidad_contacto": "Alcaldía Alto Baudó / Armada Nacional"
    }
}

PROTOCOLOS_EMERGENCIA = {
    "derrumbe": {
        "codigo": "ALERTA ROJA - MOVIMIENTO EN MASA (DERRUMBE)",
        "nivel": "CRÍTICO - NIVEL 4",
        "color": "#EF4444",
        "acciones": [
            "Cierre preventivo inmediato del corredor vial y evacuación de perímetro a 300 m.",
            "Despacho urgente de maquinaria amarilla (INVÍAS / Gestión del Riesgo Departamental).",
            "Notificación automática vía SMS/Radio a puestos de control y organismos de socorro.",
            "Inspección geotécnica de saturación del talud antes de habilitar paso."
        ]
    },
    "inundacion": {
        "codigo": "ALERTA ROJA - DESBORDAMIENTO / CRECIENTE SÚBITA",
        "nivel": "CRÍTICO - NIVEL 4",
        "color": "#F97316",
        "acciones": [
            "Activación de sirenas comunitarias en riberas bajas y zonas de inundación histórica.",
            "Evacuación preventiva hacia albergues temporales certificados por el CMGRD.",
            "Monitoreo continuo cada 15 minutos del nivel de lámina de agua.",
            "Despliegue de lanchas de rescate y brigadas de atención prehospitalaria."
        ]
    },
    "normal": {
        "codigo": "CONDICIÓN OPERATIVA NORMAL — SIN NOVEDAD",
        "nivel": "ESTABLE - NIVEL 1",
        "color": "#10B981",
        "acciones": [
            "Continuar ciclo automático de captura óptica y telemetría ambiental.",
            "Registrar evidencia en bitácora histórica sin activación de alarmas."
        ]
    }
}
