# 🛰️ SAT-CHOCÓ | Centro de Control y Alerta Temprana por Visión Artificial

Plataforma de producción diseñada para el monitoreo ambiental y detección temprana de **derrumbes (movimientos en masa)** e **inundaciones súbitas** en el departamento del Chocó.

## ✨ Características de Producción
- **Seguridad y Encapsulamiento:** Las credenciales y el endpoint de **Azure Custom Vision (`Modelo_Mejorado`)** están integrados directamente en `src/config.py`, eliminando campos técnicos en la interfaz visual.
- **Consola Tipo Centro de Operaciones (COE):** Interfaz oscura de alto contraste con monitoreo por estación georreferenciada del Chocó (Quibdó, Tadó, Carmen de Atrato, Istmina y Alto Baudó).
- **Motor de Alertas y Protocolos:** Al detectar un derrumbe o inundación por encima del umbral crítico, la plataforma activa una alerta roja animada y despliega el protocolo institucional de respuesta inmediata (INVÍAS, CMGRD, Defensa Civil).
- **Mapa Georreferenciado y Bitácora Oficial:** Visualización espacial de sensores en el Chocó y registro histórico exportable a CSV.

## 🚀 Ejecución Rápida en VS Code
```bash
pip install -r requirements.txt
streamlit run app.py
```
