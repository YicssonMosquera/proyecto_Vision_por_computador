import unicodedata
import requests
from src.config import AZURE_PREDICTION_URL, AZURE_PREDICTION_KEY


def normalizar_tag(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower().strip()


def analizar_frame(imagen_bytes: bytes) -> dict:
    if not AZURE_PREDICTION_KEY:
        raise RuntimeError(
            "Falta AZURE_PREDICTION_KEY. Configura la variable de entorno "
            "antes de ejecutar el análisis."
        )

    headers = {
        "Prediction-Key": AZURE_PREDICTION_KEY.strip(),
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(
        AZURE_PREDICTION_URL.strip(),
        headers=headers,
        data=imagen_bytes,
        timeout=25
    )
    response.raise_for_status()
    data = response.json()

    predicciones = []
    for p in data.get("predictions", []):
        clave = normalizar_tag(p["tagName"])
        predicciones.append({
            "clave": clave,
            "etiqueta": p["tagName"],
            "probabilidad": float(p["probability"])
        })

    predicciones.sort(key=lambda x: x["probabilidad"], reverse=True)
    return {
        "id": data.get("id", "N/A"),
        "timestamp": data.get("created", ""),
        "top": predicciones[0] if predicciones else None,
        "todas": predicciones
    }
