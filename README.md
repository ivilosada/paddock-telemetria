# Paddock y Pluma — Telemetría

App de telemetría en tiempo real para Fórmula 1 y Formula E con análisis IA.

## Arrancar en local

```bash
source venv/bin/activate
streamlit run app.py
```

## Estructura

| Archivo | Descripción |
|---|---|
| `app.py` | App principal |
| `pilotos_fe.py` | Diccionario de pilotos Formula E |
| `radios.py` | Módulo de radios de equipo F1 |
| `requirements.txt` | Dependencias Python |

## APIs utilizadas
- **OpenF1** — Telemetría, posiciones y radios F1
- **stats-centre.fiaformulae.com** — Datos en tiempo real FE
- **Groq (LLaMA 3.3)** — Análisis IA de sesiones y documentos FIA

## Deploy
Streamlit Cloud — rama `main` → redespliegue automático en cada push