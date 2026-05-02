import streamlit as st
import os
import requests
import base64
import time
import json
import tempfile
import pandas as pd
from urllib.parse import quote
from bs4 import BeautifulSoup
from groq import Groq
from pilotos_fe import PILOTOS_FE

st.set_page_config(
    page_title="Paddock y Pluma — Telemetría",
    page_icon="🏎️",
    layout="wide"
)

cliente = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "pagina" not in st.session_state:
    st.session_state.pagina = "welcome"

if st.session_state.pagina == "welcome":
    with open("logo_paddock.png", "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    with open("logo_f1.svg", "rb") as f:
        f1_b64 = base64.b64encode(f.read()).decode()
    with open("logo_fe.svg", "rb") as f:
        fe_b64 = base64.b64encode(f.read()).decode()

    try:
        font_response = requests.get("https://www.fiaformulae.com/resources/v4.37.8/fonts/FESans.var.woff2", timeout=5)
        font_b64 = base64.b64encode(font_response.content).decode()
        font_src = f"url(data:font/woff2;base64,{font_b64})"
    except:
        font_src = "sans-serif"

    st.markdown(f"""
    <style>
    @font-face {{
        font-family: 'FESans';
        src: {font_src};
        font-weight: 100 900;
        font-style: normal;
    }}
    .stApp {{ background: #0d0d0d !important; }}
    .welcome-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 75vh;
        text-align: center;
        gap: 2rem;
        font-family: 'FESans', 'Inter', sans-serif;
    }}
    .welcome-logo {{ width: min(600px, 85vw); opacity: 0.95; }}
    .welcome-subtitle {{
        color: rgba(255,255,255,0.5);
        font-size: 1rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: -1rem;
    }}
    .welcome-buttons {{ display: flex; justify-content: center; gap: 2rem; margin-top: 1rem; }}
    .welcome-btn {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        padding: 28px 48px;
        border-radius: 14px;
        color: white;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }}
    .welcome-btn-f1 {{ border: 1px solid rgba(255,30,0,0.4); background: rgba(255,30,0,0.06); }}
    .welcome-btn-fe {{ border: 1px solid rgba(77,110,255,0.4); background: rgba(77,110,255,0.06); }}
    .welcome-btn img {{ width: 120px; height: 48px; object-fit: contain; }}
    .welcome-btn:hover {{ transform: scale(1.04); transition: transform 0.15s ease; }}
    .welcome-btn-f1:hover {{ border-color: rgba(255,30,0,0.8) !important; background: rgba(255,30,0,0.12) !important; }}
    .welcome-btn-fe:hover {{ border-color: rgba(77,110,255,0.8) !important; background: rgba(77,110,255,0.12) !important; }}
    </style>
    <div class="welcome-container">
        <img class="welcome-logo" src="data:image/png;base64,{logo_b64}" />
        <p class="welcome-subtitle">Telemetría · Datos · IA</p>
        <div class="welcome-buttons">
            <a href="?cat=f1" class="welcome-btn welcome-btn-f1" style="text-decoration:none;cursor:pointer;">
                <img src="data:image/svg+xml;base64,{f1_b64}" />
                Fórmula 1
            </a>
            <a href="?cat=fe" class="welcome-btn welcome-btn-fe" style="text-decoration:none;cursor:pointer;">
                <img src="data:image/svg+xml;base64,{fe_b64}" />
                Formula E
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Detectar click en logo vía query params
    params = st.query_params
    if params.get("cat") == "f1":
        st.session_state.pagina = "f1"
        st.query_params.clear()
        st.rerun()
    elif params.get("cat") == "fe":
        st.session_state.pagina = "fe"
        st.query_params.clear()
        st.rerun()

    
    st.stop()

categoria = "Fórmula 1" if st.session_state.pagina == "f1" else "Formula E"

# Botón de volver
if st.button("← Volver al inicio"):
    st.session_state.pagina = "welcome"
    st.rerun()

# Estilos según categoría
if categoria == "Fórmula 1":
    accent = "#e10600"
    accent2 = "#ff4d4d"
    grad_start = "#0d0d0d"
    grad_end = "#1a0000"
else:
    accent = "#4d6eff"
    accent2 = "#00b4ff"
    grad_start = "#0d0d0d"
    grad_end = "#000d1a"

try:
    font_resp = requests.get("https://www.fiaformulae.com/resources/v4.37.8/fonts/FESans.var.woff2", timeout=5)
    font_face = f"url(data:font/woff2;base64,{base64.b64encode(font_resp.content).decode()})"
except:
    font_face = "sans-serif"

st.markdown(f"""<style>
@font-face {{ font-family: 'FESans'; src: {font_face}; font-weight: 100 900; font-style: normal; }}
html, body, [class*="css"], h1, h2, h3, h4, p, label, button, div {{
    font-family: 'FESans', 'Inter', sans-serif !important;
}}
.stApp {{ background: linear-gradient(160deg, {grad_start} 0%, {grad_end} 100%) !important; background-attachment: fixed !important; }}
.stApp h1 {{ font-size: 2.2rem !important; font-weight: 800 !important; color: #ffffff !important; }}
.stApp h2, .stApp h3 {{ color: #ffffff !important; font-weight: 700 !important; }}
.stApp p, .stApp label, .stApp div {{ color: rgba(255,255,255,0.9) !important; }}
.stButton > button {{ background: linear-gradient(90deg, {accent}, {accent2}) !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; padding: 10px 20px !important; }}
[data-testid="metric-container"] {{ background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 12px !important; padding: 16px !important; }}
[data-testid="metric-container"] label {{ color: rgba(255,255,255,0.6) !important; font-size: 0.75rem !important; text-transform: uppercase !important; }}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{ color: #ffffff !important; font-size: 1.8rem !important; font-weight: 800 !important; }}
[data-baseweb="select"] > div {{ background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.2) !important; border-radius: 8px !important; color: #ffffff !important; }}
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea {{ background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.2) !important; border-radius: 8px !important; color: #ffffff !important; }}
[data-testid="stDataFrame"] {{ border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 12px !important; overflow: hidden !important; }}
[data-testid="stAlert"] {{ background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 12px !important; color: #ffffff !important; }}
[data-testid="stExpander"] {{ background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; }}
hr {{ border-color: rgba(255,255,255,0.1) !important; }}
.flag-badge {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}}
.flag-green {{ background: rgba(0,200,80,0.2); border: 1px solid rgba(0,200,80,0.5); color: #00c850; }}
.flag-yellow {{ background: rgba(255,200,0,0.2); border: 1px solid rgba(255,200,0,0.5); color: #ffc800; }}
.flag-red {{ background: rgba(255,30,0,0.2); border: 1px solid rgba(255,30,0,0.5); color: #ff1e00; }}
.flag-sc {{ background: rgba(255,150,0,0.2); border: 1px solid rgba(255,150,0,0.5); color: #ff9600; }}
.flag-chequered {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.3); color: #ffffff; }}
.attack-active {{ background: rgba(0,180,255,0.2); border: 1px solid rgba(0,180,255,0.5); color: #00b4ff; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }}
.attack-inactive {{ color: rgba(255,255,255,0.3); font-size: 0.75rem; }}
.doc-item {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px 14px; margin: 4px 0; display: flex; justify-content: space-between; align-items: center; }}
.doc-decision {{ border-left: 3px solid #ff9600; }}
.doc-classification {{ border-left: 3px solid #00c850; }}
.doc-technical {{ border-left: 3px solid #4d6eff; }}
</style>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── FUNCIONES OPENF1 (F1) ────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=60)
def obtener_sesion_activa_f1():
    """
    Detecta automáticamente la sesión activa o más reciente de F1.
    Usa el Index.json de LiveTiming para obtener el meeting activo,
    y OpenF1 para los datos de telemetría.
    """
    from datetime import datetime, timezone, timedelta
    try:
        # Obtener el Index.json de LiveTiming (fuente de verdad para el evento activo)
        r = requests.get(
            "https://livetiming.formula1.com/static/2026/Index.json",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        if r.status_code == 200:
            data = json.loads(r.content.decode('utf-8-sig'))
            meetings = data.get('Meetings', [])
            ahora = datetime.now(timezone.utc)

            # Encontrar el meeting activo o más reciente
            meeting_activo = None
            sesion_activa = None

            for meeting in meetings:
                for sesion in meeting.get('Sessions', []):
                    start_str = sesion.get('StartDate', '')
                    end_str = sesion.get('EndDate', '')
                    gmt_offset = sesion.get('GmtOffset', '00:00:00')

                    if not start_str:
                        continue

                    try:
                        # Parsear offset GMT
                        parts = gmt_offset.split(':')
                        offset_h = int(parts[0])
                        offset_m = int(parts[1]) if len(parts) > 1 else 0
                        offset = timedelta(hours=offset_h, minutes=offset_m)
                        tz = timezone(offset)

                        t_inicio = datetime.fromisoformat(start_str).replace(tzinfo=tz).astimezone(timezone.utc)
                        t_fin = datetime.fromisoformat(end_str).replace(tzinfo=tz).astimezone(timezone.utc) if end_str else t_inicio + timedelta(hours=3)

                        if t_inicio <= ahora <= t_fin:
                            meeting_activo = meeting
                            sesion_activa = sesion
                            sesion_activa['_live'] = True
                            sesion_activa['_meeting'] = meeting
                            break
                    except:
                        pass

                if sesion_activa:
                    break

            # Si no hay sesión en vivo, buscar la más reciente que ya haya empezado
            if not sesion_activa:
                candidatas = []
                for meeting in meetings:
                    for sesion in meeting.get('Sessions', []):
                        start_str = sesion.get('StartDate', '')
                        gmt_offset = sesion.get('GmtOffset', '00:00:00')
                        if not start_str:
                            continue
                        try:
                            parts = gmt_offset.split(':')
                            offset_h = int(parts[0])
                            offset_m = int(parts[1]) if len(parts) > 1 else 0
                            offset = timedelta(hours=offset_h, minutes=offset_m)
                            tz = timezone(offset)
                            t_inicio = datetime.fromisoformat(start_str).replace(tzinfo=tz).astimezone(timezone.utc)
                            if t_inicio <= ahora:
                                s = dict(sesion)
                                s['_live'] = False
                                s['_meeting'] = meeting
                                s['_t_inicio'] = t_inicio
                                candidatas.append(s)
                        except:
                            pass

                if candidatas:
                    candidatas.sort(key=lambda x: x['_t_inicio'], reverse=True)
                    sesion_activa = candidatas[0]

            if sesion_activa:
                # Obtener el session_key de OpenF1 para esta sesión
                meeting = sesion_activa.get('_meeting', {})
                location = meeting.get('Location', '')
                session_name = sesion_activa.get('Name', '')

                # Buscar en OpenF1 la sesión correspondiente
                r2 = requests.get(
                    f"https://api.openf1.org/v1/sessions?year=2026&location={location}",
                    timeout=10
                )
                if r2.status_code == 200 and r2.json():
                    sesiones_openf1 = r2.json()
                    # Buscar la sesión que coincida por nombre
                    sesion_openf1 = None
                    for s in sesiones_openf1:
                        if s.get('session_name', '').lower() == session_name.lower():
                            sesion_openf1 = s
                            break
                    # Si no coincide exactamente, usar la más reciente
                    if not sesion_openf1:
                        from datetime import datetime, timezone
                        ahora2 = datetime.now(timezone.utc)
                        validas = []
                        for s in sesiones_openf1:
                            try:
                                t = datetime.fromisoformat(s['date_start'].replace('Z', '+00:00'))
                                if t <= ahora2:
                                    validas.append((t, s))
                            except:
                                pass
                        if validas:
                            validas.sort(key=lambda x: x[0], reverse=True)
                            sesion_openf1 = validas[0][1]

                    if sesion_openf1:
                        sesion_openf1['_live'] = sesion_activa.get('_live', False)
                        sesion_openf1['_meeting_name'] = meeting.get('Name', location)
                        sesion_openf1['_meeting_location'] = location
                        sesion_openf1['_livetiming_path'] = sesion_activa.get('Path', '')
                        return sesion_openf1

        # Fallback: usar OpenF1 directamente
        r = requests.get("https://api.openf1.org/v1/sessions?year=2026", timeout=10)
        if r.status_code == 200:
            sesiones = r.json()
            if not sesiones:
                return None
            from datetime import datetime, timezone
            ahora = datetime.now(timezone.utc)
            sesiones_validas = []
            for s in sesiones:
                if s.get('session_key') and s.get('date_start'):
                    try:
                        t = datetime.fromisoformat(s['date_start'].replace('Z', '+00:00'))
                        if t <= ahora:
                            sesiones_validas.append((t, s))
                    except:
                        pass
            if sesiones_validas:
                sesiones_validas.sort(key=lambda x: x[0], reverse=True)
                ultima = sesiones_validas[0][1]
                ultima['_live'] = False
                return ultima

    except Exception as e:
        st.error(f"Error al conectar con la API: {e}")
    return None


@st.cache_data(ttl=3600)
def obtener_nombres_jolpica():
    try:
        r = requests.get("https://api.jolpi.ca/ergast/f1/2026/races.json", timeout=10)
        carreras = r.json()["MRData"]["RaceTable"]["Races"]
        nombres = {}
        for c in carreras:
            nombres[c["Circuit"]["Location"]["country"]] = c["raceName"]
            nombres[c["Circuit"]["Location"]["locality"]] = c["raceName"]
            nombres[c["circuitId"]] = c["raceName"]
        return nombres
    except:
        return {}


def obtener_posiciones(session_key):
    r = requests.get(f"https://api.openf1.org/v1/position?session_key={session_key}")
    return r.json() if r.status_code == 200 else []


def obtener_pilotos(session_key):
    r = requests.get(f"https://api.openf1.org/v1/drivers?session_key={session_key}")
    return r.json() if r.status_code == 200 else []


def obtener_vueltas(session_key):
    r = requests.get(f"https://api.openf1.org/v1/laps?session_key={session_key}")
    return r.json() if r.status_code == 200 else []


def obtener_telemetria_piloto(session_key, driver_number):
    r = requests.get(f"https://api.openf1.org/v1/car_data?session_key={session_key}&driver_number={driver_number}")
    return r.json() if r.status_code == 200 else []


def obtener_stints(session_key):
    r = requests.get(f"https://api.openf1.org/v1/stints?session_key={session_key}")
    return r.json() if r.status_code == 200 else []


@st.cache_data(ttl=60)
def obtener_radios(session_key):
    """Obtiene las radios del equipo de la sesión actual desde OpenF1."""
    try:
        r = requests.get(
            f"https://api.openf1.org/v1/team_radio?session_key={session_key}",
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                return data
    except:
        pass
    return []


def formato_tiempo(segundos):
    if not segundos:
        return "—"
    m = int(segundos // 60)
    s = segundos % 60
    return f"{m}:{s:06.3f}" if m > 0 else f"{s:.3f}s"


# ══════════════════════════════════════════════════════════════════════════════
# ── FUNCIONES DOCUMENTOS FIA F1 (DINÁMICO) ───────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300)
def obtener_docs_fia_f1(location=None):
    """
    Obtiene los documentos FIA de F1 para el evento activo.
    Scraping de fia.com/documents/championships/fia-formula-one-world-championship-14/
    Devuelve lista de dicts: {titulo, url, tipo}
    """
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0'}
    BASE_FIA = "https://www.fia.com"
    CHAMP_URL = f"{BASE_FIA}/documents/championships/fia-formula-one-world-championship-14/"

    try:
        r = requests.get(CHAMP_URL, headers=headers, timeout=15)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')
        docs = []

        # Buscar los links de documentos del evento actual (los primeros en la página)
        for a in soup.find_all('a', href=True):
            href = a['href']
            texto = a.get_text(strip=True)

            # PDFs directos
            if '/system/files/decision-document/' in href and href.endswith('.pdf'):
                url_completa = BASE_FIA + href if href.startswith('/') else href
                tipo = _clasificar_doc_f1(texto)
                docs.append({'titulo': texto, 'url': url_completa, 'tipo': tipo})

            # Links a listas de documentos por evento
            elif '/decision-document-list/nojs/' in href and texto:
                # Solo el primer evento (el actual)
                if len([d for d in docs if d.get('_es_lista')]) == 0:
                    url_lista = BASE_FIA + href if href.startswith('/') else href
                    docs_evento = _obtener_docs_lista_fia(url_lista, headers, BASE_FIA)
                    for d in docs_evento:
                        d['_es_lista'] = True
                        docs.append(d)
                    break

        return docs[:50]  # Limitar a 50 documentos
    except Exception as e:
        return []


def _obtener_docs_lista_fia(url_lista, headers, base_url):
    """Obtiene los documentos de una lista de documentos FIA."""
    try:
        r = requests.get(url_lista, headers=headers, timeout=10)
        if r.status_code != 200:
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        docs = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            texto = a.get_text(strip=True)
            if '/system/files/decision-document/' in href and href.endswith('.pdf'):
                url_completa = base_url + href if href.startswith('/') else href
                tipo = _clasificar_doc_f1(texto)
                docs.append({'titulo': texto, 'url': url_completa, 'tipo': tipo})
        return docs
    except:
        return []


def _clasificar_doc_f1(titulo):
    t = titulo.upper()
    if any(x in t for x in ['DECISION', 'PENALTY', 'SANCTION', 'INFRINGEMENT']):
        return 'decision'
    elif any(x in t for x in ['CLASSIFICATION', 'RESULT', 'GRID', 'STANDINGS']):
        return 'classification'
    elif any(x in t for x in ['TECHNICAL', 'SCRUTINEER', 'EXCLUSION']):
        return 'technical'
    elif any(x in t for x in ['DIRECTOR', 'RACE DIRECTOR', 'BULLETIN', 'NOTE']):
        return 'note'
    return 'general'


# ══════════════════════════════════════════════════════════════════════════════
# ── FUNCIONES DOCUMENTOS FIA FORMULA E (DINÁMICO) ────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

FE_DOCS_BASE = "https://results.formulae.fia.com"
FE_DOCS_HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}


@st.cache_data(ttl=300)
def obtener_eventos_fe_docs():
    """Obtiene la lista de eventos disponibles en el notice board de Formula E."""
    try:
        # Obtener temporada actual (Season 12 = 2025-26)
        r = requests.get(
            f"{FE_DOCS_BASE}/api/getindex/formula-e/files/noticeboard",
            headers=FE_DOCS_HEADERS, timeout=10
        )
        if r.status_code != 200:
            return []

        data = r.json()
        # Buscar la temporada más reciente
        temporadas = data.get('items', [])
        if not temporadas:
            return []

        temporada_actual = temporadas[0]  # La primera es la más reciente

        # Obtener los eventos de esa temporada
        r2 = requests.get(
            f"{FE_DOCS_BASE}/api/getindex/{quote(temporada_actual['id'])}",
            headers=FE_DOCS_HEADERS, timeout=10
        )
        if r2.status_code != 200:
            return []

        eventos = r2.json().get('items', [])
        return [(e['title'], e['id']) for e in eventos]
    except:
        return []


@st.cache_data(ttl=120)
def obtener_docs_fe_evento(evento_id):
    """
    Obtiene todos los documentos de un evento de Formula E del notice board.
    Devuelve lista de dicts: {titulo, id, tipo, url_descarga}
    """
    try:
        r = requests.get(
            f"{FE_DOCS_BASE}/api/getindex/{quote(evento_id)}",
            headers=FE_DOCS_HEADERS, timeout=10
        )
        if r.status_code != 200:
            return []

        docs = []
        for item in r.json().get('items', []):
            if item.get('extention') == 'pdf':
                url_descarga = f"{FE_DOCS_BASE}/api/getfile/{item['id']}"
                tipo = _clasificar_doc_fe(item['title'])
                docs.append({
                    'titulo': item['title'],
                    'id': item['id'],
                    'tipo': tipo,
                    'url': url_descarga
                })
        return docs
    except:
        return []


def _clasificar_doc_fe(titulo):
    t = titulo.upper()
    if any(x in t for x in ['DECISION', 'PENALTY']):
        return 'decision'
    elif any(x in t for x in ['CLASSIFICATION', 'RESULT', 'GRID', 'STARTING']):
        return 'classification'
    elif any(x in t for x in ['TECHNICAL', 'SCRUTINEER']):
        return 'technical'
    elif any(x in t for x in ['BULLETIN', 'NOTE', 'INFORMATION', 'ENTRY LIST']):
        return 'note'
    return 'general'


def _icono_tipo_doc(tipo):
    iconos = {
        'decision': '⚖️',
        'classification': '🏁',
        'technical': '🔧',
        'note': '📋',
        'general': '📄'
    }
    return iconos.get(tipo, '📄')


def analizar_pdf_con_groq(url_pdf, titulo, contexto=""):
    """Descarga un PDF y lo analiza con Groq."""
    try:
        r = requests.get(url_pdf, timeout=20, headers=FE_DOCS_HEADERS)
        if r.status_code != 200:
            return f"No se pudo descargar el documento ({r.status_code})."

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(r.content)
            tmp_path = tmp.name

        # Extraer texto del PDF con pdftotext
        import subprocess
        result = subprocess.run(
            ['pdftotext', tmp_path, '-'],
            capture_output=True, text=True, timeout=30
        )
        os.unlink(tmp_path)

        texto_pdf = result.stdout.strip()
        if not texto_pdf:
            return "No se pudo extraer texto del PDF."

        # Limitar el texto a 3000 caracteres para el prompt
        texto_truncado = texto_pdf[:3000]

        prompt = f"""Eres un experto en reglamento de motorsport. Analiza este documento FIA{' de ' + contexto if contexto else ''}:

Título: {titulo}

Contenido:
{texto_truncado}

Explica en 3-4 frases claras y directas qué dice este documento, qué implica para el campeonato y si hay algo importante que los aficionados deban saber. Habla en español, con tono periodístico."""

        respuesta = cliente.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        return f"Error al analizar el documento: {e}"


# ══════════════════════════════════════════════════════════════════════════════
# ── FUNCIONES FORMULA E ───────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

FE_BASE = "https://stats-centre.fiaformulae.com/prod/api"


@st.cache_data(ttl=30)
def obtener_standings_fe():
    try:
        r = requests.get(f"{FE_BASE}/realtime/standings", timeout=10, verify=False)
        if r.status_code == 200:
            return r.json().get("data", {}).get("standings", {})
    except:
        pass
    return {}


@st.cache_data(ttl=30)
def obtener_championship_info_fe():
    """Obtiene los IDs activos de championship, event y session."""
    try:
        r = requests.get(f"{FE_BASE}/realtime/standings", timeout=10, verify=False)
        if r.status_code == 200:
            data = r.json().get("data", {})
            return data.get("championship_info", {})
    except:
        pass
    return {}


@st.cache_data(ttl=60)
def obtener_estado_sesion_fe():
    """Obtiene el estado de la sesión de Formula E."""
    try:
        r = requests.get(f"{FE_BASE}/utils/status", timeout=10, verify=False)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return {}


@st.cache_data(ttl=30)
def obtener_mejores_vueltas_fe(championship_id, event_id):
    url = f"{FE_BASE}/details/best-lap-timings?championshipId={championship_id}&eventId={event_id}"
    try:
        r = requests.get(url, timeout=10, verify=False)
        if r.status_code == 200:
            data = r.json().get("data", [])
            if data:
                return data[0].get("participants", {})
    except:
        pass
    return {}


@st.cache_data(ttl=30)
def obtener_sectores_fe(championship_id, event_id):
    url = f"{FE_BASE}/details/sectortiming?championshipId={championship_id}&eventId={event_id}"
    try:
        r = requests.get(url, timeout=10, verify=False)
        if r.status_code == 200:
            data = r.json().get("data", [])
            if data:
                return data[0].get("participants", {})
    except:
        pass
    return {}


@st.cache_data(ttl=60)
def obtener_finishline_fe(championship_id, event_id):
    url = f"{FE_BASE}/details/finishline?championshipId={championship_id}&eventId={event_id}"
    try:
        r = requests.get(url, timeout=10, verify=False)
        if r.status_code == 200:
            return r.json().get("data", [])
    except:
        pass
    return []


@st.cache_data(ttl=30)
def obtener_feature_info_fe():
    try:
        r = requests.get(f"{FE_BASE}/realtime/feature-info", timeout=10, verify=False)
        if r.status_code == 200:
            return r.json().get("data", {})
    except:
        pass
    return {}


def ms_a_tiempo(ms):
    if not ms:
        return "—"
    segundos = ms / 1000
    minutos = int(segundos // 60)
    segs = segundos % 60
    return f"{minutos}:{segs:06.3f}" if minutos > 0 else f"{segs:.3f}s"


def render_flag_badge(flag_text):
    flag_upper = str(flag_text).upper()
    if "GREEN" in flag_upper:
        return '<span class="flag-badge flag-green">🟢 Bandera Verde</span>'
    elif "YELLOW" in flag_upper:
        return '<span class="flag-badge flag-yellow">🟡 Bandera Amarilla</span>'
    elif "RED" in flag_upper:
        return '<span class="flag-badge flag-red">🔴 Bandera Roja</span>'
    elif "SAFETY" in flag_upper or flag_upper in ("SC", "VSC"):
        label = "🟠 VSC" if "VSC" in flag_upper else "🟠 Safety Car"
        return f'<span class="flag-badge flag-sc">{label}</span>'
    elif "CHEQUERED" in flag_upper or "CHECKER" in flag_upper:
        return '<span class="flag-badge flag-chequered">🏁 Bandera a Cuadros</span>'
    return f'<span class="flag-badge flag-green">⚑ {flag_text}</span>'


# ══════════════════════════════════════════════════════════════════════════════
# ── FUNCIONES TRAZADO CIRCUITO Y RACE CONTROL F1 ─────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
import io

@st.cache_data(ttl=86400)  # Cache 24h — el trazado no cambia
def generar_trazado_circuito_f1(session_key, driver_number=1):
    """
    Genera el trazado del circuito de F1 desde datos GPS de OpenF1.
    Devuelve la imagen como base64 PNG.
    """
    try:
        r = requests.get(
            f"https://api.openf1.org/v1/location?session_key={session_key}&driver_number={driver_number}",
            timeout=20
        )
        if r.status_code != 200:
            return None
        data = r.json()
        if not isinstance(data, list) or len(data) < 100:
            return None

        xs = np.array([p["x"] for p in data if "x" in p and "y" in p], dtype=float)
        ys = np.array([p["y"] for p in data if "x" in p and "y" in p], dtype=float)
        if len(xs) < 100:
            return None

        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#0d0d0d')
        ax.set_facecolor('#0d0d0d')
        ax.plot(xs, ys, color='#e10600', linewidth=2.5, alpha=0.9,
                path_effects=[pe.Stroke(linewidth=6, foreground='#ffffff', alpha=0.07), pe.Normal()])
        ax.scatter([xs[0]], [ys[0]], color='#ffffff', s=50, zorder=5)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.tight_layout(pad=0)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=110, bbox_inches='tight',
                    facecolor='#0d0d0d', edgecolor='none')
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode()
    except:
        return None


@st.cache_data(ttl=30)
def obtener_race_control_f1(session_key):
    """Obtiene los mensajes de Race Control (banderas) de la sesión actual."""
    try:
        r = requests.get(
            f"https://api.openf1.org/v1/race_control?session_key={session_key}",
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list):
                return data
    except:
        pass
    return []


def obtener_bandera_actual_f1(race_control_msgs):
    """Extrae la bandera más reciente de los mensajes de Race Control."""
    if not race_control_msgs:
        return "GREEN"
    # Buscar el último mensaje con bandera
    for msg in reversed(race_control_msgs):
        flag = msg.get("flag", "") or ""
        if flag and flag not in ("", "NONE", "CLEAR"):
            return flag
    return "GREEN"


# ══════════════════════════════════════════════════════════════════════════════
# ── BLOQUE FÓRMULA 1 ──────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

if categoria == "Fórmula 1":

    sesion = obtener_sesion_activa_f1()

    if sesion:
        nombre_carrera = sesion.get("_meeting_location") or sesion.get("location") or "Gran Premio"
        nombre_sesion = sesion.get("session_name") or "Sesión"
        es_en_vivo = sesion.get("_live", False)
        nombres_oficiales = obtener_nombres_jolpica()
        nombre_oficial = sesion.get("_meeting_name") or nombres_oficiales.get(nombre_carrera, nombre_carrera)

        if es_en_vivo:
            st.markdown('<span style="background:rgba(255,30,0,0.2);border:1px solid rgba(255,30,0,0.5);color:#ff1e00;padding:4px 12px;border-radius:20px;font-weight:700;font-size:0.8rem;">● EN DIRECTO</span>', unsafe_allow_html=True)
            st.markdown("")

        st.subheader(f"⚡ {nombre_oficial} — {nombre_sesion}")
        session_key = sesion.get("session_key")

        # ──────────────────────────────────────────────────────────────────────────────
        # Panel de estado de sesión (estilo Formula E)
        # ──────────────────────────────────────────────────────────────────────────────
        st.subheader("Estado de la sesión")

        race_control_msgs = obtener_race_control_f1(session_key)
        bandera_actual = obtener_bandera_actual_f1(race_control_msgs)
        badge_bandera = render_flag_badge(bandera_actual)

        # Contar vueltas completadas (máximo de vueltas entre todos los pilotos)
        # Usamos los datos de posición para saber la vuelta actual
        vueltas_raw_estado = obtener_vueltas(session_key)
        max_vuelta = 0
        if vueltas_raw_estado and isinstance(vueltas_raw_estado, list):
            for v in vueltas_raw_estado:
                ln = v.get("lap_number") or 0
                if ln > max_vuelta:
                    max_vuelta = ln

        # Total de vueltas de la sesión (de OpenF1 o estimado)
        total_vueltas = sesion.get("total_laps") or "?"

        # Tipo de sesión para el badge
        tipo_sesion = sesion.get("session_type", "") or ""
        if tipo_sesion.upper() == "RACE" or "RACE" in nombre_sesion.upper():
            badge_sesion = '<span style="background:rgba(255,30,0,0.15);border:1px solid rgba(255,30,0,0.4);color:#ff6b6b;padding:3px 10px;border-radius:20px;font-weight:700;font-size:0.75rem;">CARRERA</span>'
        elif "QUALI" in nombre_sesion.upper():
            badge_sesion = '<span style="background:rgba(255,200,0,0.15);border:1px solid rgba(255,200,0,0.4);color:#ffc800;padding:3px 10px;border-radius:20px;font-weight:700;font-size:0.75rem;">CLASIFICACIÓN</span>'
        elif "SPRINT" in nombre_sesion.upper():
            badge_sesion = '<span style="background:rgba(77,110,255,0.15);border:1px solid rgba(77,110,255,0.4);color:#7b9fff;padding:3px 10px;border-radius:20px;font-weight:700;font-size:0.75rem;">SPRINT</span>'
        elif "PRACTICE" in nombre_sesion.upper() or "FREE" in nombre_sesion.upper():
            badge_sesion = '<span style="background:rgba(0,200,80,0.12);border:1px solid rgba(0,200,80,0.35);color:#00c850;padding:3px 10px;border-radius:20px;font-weight:700;font-size:0.75rem;">ENTRENAMIENTOS</span>'
        else:
            badge_sesion = f'<span style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.7);padding:3px 10px;border-radius:20px;font-weight:700;font-size:0.75rem;">{nombre_sesion.upper()}</span>'

        if not es_en_vivo:
            badge_sesion = '<span style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.4);padding:3px 10px;border-radius:20px;font-weight:700;font-size:0.75rem;">SIN SESIÓN ACTIVA</span>'

        # Modo en directo toggle
        modo_directo_f1 = st.toggle("Modo en directo", value=es_en_vivo, key="toggle_directo_f1")

        # Fila de estado: badge sesión | bandera | vueltas | mapa
        col_estado1, col_estado2, col_estado3, col_estado4 = st.columns([2, 2, 2, 3])

        with col_estado1:
            st.markdown(badge_sesion, unsafe_allow_html=True)

        with col_estado2:
            st.markdown(badge_bandera, unsafe_allow_html=True)

        with col_estado3:
            if max_vuelta > 0:
                st.markdown('<span style="color:rgba(255,255,255,0.4);font-size:0.75rem;">Vueltas completadas</span>', unsafe_allow_html=True)
                st.markdown(f'<span style="font-size:2rem;font-weight:800;color:#ffffff;">{max_vuelta}</span>', unsafe_allow_html=True)
                if total_vueltas and total_vueltas != "?":
                    st.caption(f"de {total_vueltas} programadas")
            else:
                st.markdown('<span style="color:rgba(255,255,255,0.3);font-size:0.85rem;">Vueltas: —</span>', unsafe_allow_html=True)

        with col_estado4:
            # Generar trazado del circuito desde datos GPS
            img_circuito = generar_trazado_circuito_f1(session_key)
            if img_circuito:
                st.markdown(
                    f'<img src="data:image/png;base64,{img_circuito}" style="width:100%;border-radius:8px;opacity:0.9;"/>',
                    unsafe_allow_html=True
                )
                circuito_nombre = sesion.get("circuit_short_name") or nombre_carrera
                st.caption(f"Circuito — {circuito_nombre}")
            else:
                st.markdown('<span style="color:rgba(255,255,255,0.2);font-size:0.8rem;">Mapa no disponible</span>', unsafe_allow_html=True)

        st.markdown("---")

        pilotos = obtener_pilotos(session_key)
        posiciones_raw = obtener_posiciones(session_key)
        vueltas_raw = obtener_vueltas(session_key)
        pilotos_dict = {p["driver_number"]: p for p in pilotos}

        ultimas_posiciones = {}
        for pos in posiciones_raw:
            ultimas_posiciones[pos["driver_number"]] = pos

        mejores_vueltas = {}
        for vuelta in vueltas_raw:
            numero = vuelta.get("driver_number")
            tiempo = vuelta.get("lap_duration")
            if numero and tiempo:
                if numero not in mejores_vueltas or tiempo < mejores_vueltas[numero]:
                    mejores_vueltas[numero] = tiempo

        clasificacion = sorted(ultimas_posiciones.values(), key=lambda x: x.get("position", 99))

        orden_pilotos = []
        for entrada in clasificacion:
            numero = entrada.get("driver_number")
            piloto_info = pilotos_dict.get(numero, {})
            orden_pilotos.append(piloto_info.get("full_name", f"#{numero}"))

        # Tabla de clasificación
        filas = []
        for entrada in clasificacion:
            numero = entrada.get("driver_number")
            piloto_info = pilotos_dict.get(numero, {})
            nombre = piloto_info.get("full_name", f"#{numero}")
            equipo = piloto_info.get("team_name", "—")
            posicion = entrada.get("position", "—")
            mejor_vuelta = mejores_vueltas.get(numero)
            tiempo_str = formato_tiempo(mejor_vuelta)
            filas.append({
                "Pos": posicion,
                "_numero": numero if numero else "—",
                "Piloto": nombre,
                "Equipo": equipo,
                "Mejor vuelta": tiempo_str,
            })

        if filas:
            st.subheader("Clasificación")

            # Cabecera de tabla estilo Formula E
            col1, col2, col3, col4, col5 = st.columns([1, 1, 3, 3, 2])
            col1.markdown('<span style="color:rgba(255,255,255,0.4);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;">Pos</span>', unsafe_allow_html=True)
            col2.markdown('<span style="color:rgba(255,255,255,0.4);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;">#</span>', unsafe_allow_html=True)
            col3.markdown('<span style="color:rgba(255,255,255,0.4);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;">Piloto</span>', unsafe_allow_html=True)
            col4.markdown('<span style="color:rgba(255,255,255,0.4);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;">Equipo</span>', unsafe_allow_html=True)
            col5.markdown('<span style="color:rgba(255,255,255,0.4);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;">Mejor vuelta</span>', unsafe_allow_html=True)

            for fila in filas:
                pos = fila["Pos"]
                numero = fila.get("_numero", "")
                nombre = fila["Piloto"]
                equipo = fila["Equipo"]
                tiempo = fila["Mejor vuelta"]

                # Color de posición: top 3 con colores especiales
                if pos == 1:
                    pos_color = "#ffd700"
                    pos_bg = "rgba(255,215,0,0.15)"
                elif pos == 2:
                    pos_color = "#c0c0c0"
                    pos_bg = "rgba(192,192,192,0.10)"
                elif pos == 3:
                    pos_color = "#cd7f32"
                    pos_bg = "rgba(205,127,50,0.10)"
                else:
                    pos_color = "rgba(255,255,255,0.8)"
                    pos_bg = "rgba(255,255,255,0.03)"

                col1, col2, col3, col4, col5 = st.columns([1, 1, 3, 3, 2])
                col1.markdown(
                    f'<div style="background:{pos_bg};border-radius:6px;padding:6px 10px;text-align:center;font-weight:800;color:{pos_color};font-size:1rem;">{pos}</div>',
                    unsafe_allow_html=True
                )
                col2.markdown(
                    f'<div style="padding:6px 4px;color:rgba(255,255,255,0.5);font-size:0.85rem;font-weight:600;">{numero}</div>',
                    unsafe_allow_html=True
                )
                col3.markdown(
                    f'<div style="padding:6px 4px;font-weight:700;color:#ffffff;">{nombre}</div>',
                    unsafe_allow_html=True
                )
                col4.markdown(
                    f'<div style="padding:6px 4px;color:rgba(255,255,255,0.65);font-size:0.9rem;">{equipo}</div>',
                    unsafe_allow_html=True
                )
                col5.markdown(
                    f'<div style="padding:6px 4px;font-family:monospace;color:rgba(255,255,255,0.85);font-size:0.9rem;">{tiempo}</div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")

        # Telemetría individual
        with st.expander("📊 Telemetría individual"):
            if orden_pilotos:
                piloto_sel = st.selectbox("Selecciona piloto", orden_pilotos)
                numero_sel = next(
                    (p["driver_number"] for p in pilotos if p.get("full_name") == piloto_sel),
                    None
                )
                if numero_sel:
                    datos_tel = obtener_telemetria_piloto(session_key, numero_sel)
                    if datos_tel:
                        velocidades = [d.get("speed", 0) for d in datos_tel if d.get("speed")]
                        rpm_vals = [d.get("rpm", 0) for d in datos_tel if d.get("rpm")]

                        if velocidades:
                            col_a, col_b, col_c = st.columns(3)
                            col_a.metric("Velocidad máx.", f"{max(velocidades)} km/h")
                            col_b.metric("Velocidad media", f"{sum(velocidades)//len(velocidades)} km/h")
                            col_c.metric("RPM máx.", f"{max(rpm_vals):,}" if rpm_vals else "—")
                            st.line_chart(
                                pd.DataFrame({"Velocidad (km/h)": velocidades[:500]}),
                                x_label="Muestra", y_label="Velocidad (km/h)"
                            )
                    else:
                        st.info("No hay datos de telemetría disponibles para este piloto.")

        # Comparativa de pilotos
        with st.expander("⚔️ Comparativa de pilotos"):
            if len(orden_pilotos) >= 2:
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    piloto_a = st.selectbox("Piloto A", orden_pilotos, key="cmp_a")
                with col_p2:
                    piloto_b = st.selectbox("Piloto B", orden_pilotos, index=1, key="cmp_b")

                if st.button("Comparar"):
                    num_a = next((p["driver_number"] for p in pilotos if p.get("full_name") == piloto_a), None)
                    num_b = next((p["driver_number"] for p in pilotos if p.get("full_name") == piloto_b), None)
                    tel_a = obtener_telemetria_piloto(session_key, num_a) if num_a else []
                    tel_b = obtener_telemetria_piloto(session_key, num_b) if num_b else []
                    vel_a = [d.get("speed", 0) for d in tel_a if d.get("speed")]
                    vel_b = [d.get("speed", 0) for d in tel_b if d.get("speed")]
                    mejor_a = mejores_vueltas.get(num_a)
                    mejor_b = mejores_vueltas.get(num_b)

                    if vel_a and vel_b:
                        vel_max_a, vel_media_a = max(vel_a), sum(vel_a) // len(vel_a)
                        vel_max_b, vel_media_b = max(vel_b), sum(vel_b) // len(vel_b)
                        df_comp = pd.DataFrame({
                            "Métrica": ["Velocidad máxima", "Velocidad media", "Mejor vuelta"],
                            piloto_a: [f"{vel_max_a} km/h", f"{vel_media_a} km/h", formato_tiempo(mejor_a)],
                            piloto_b: [f"{vel_max_b} km/h", f"{vel_media_b} km/h", formato_tiempo(mejor_b)],
                        })
                        st.dataframe(df_comp, use_container_width=True, hide_index=True)
                        longitud = min(len(vel_a), len(vel_b), 500)
                        st.line_chart(
                            pd.DataFrame({piloto_a: vel_a[:longitud], piloto_b: vel_b[:longitud]}),
                            x_label="Muestra de telemetría", y_label="Velocidad (km/h)"
                        )
                        prompt_comp = f"""Eres un ingeniero de carrera experto de Fórmula 1. Compara el rendimiento de estos dos pilotos en el {nombre_oficial} ({nombre_sesion}): {piloto_a}: velocidad máxima {vel_max_a} km/h, velocidad media {vel_media_a} km/h, mejor vuelta {formato_tiempo(mejor_a)}. {piloto_b}: velocidad máxima {vel_max_b} km/h, velocidad media {vel_media_b} km/h, mejor vuelta {formato_tiempo(mejor_b)}. Analiza en 3-4 frases quién tuvo mejor rendimiento y por qué, con criterio técnico y pasión. Habla en español."""
                        respuesta_comp = cliente.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": prompt_comp}],
                            max_tokens=512
                        )
                        st.info(respuesta_comp.choices[0].message.content)
                    else:
                        st.warning("No hay datos de telemetría disponibles para uno o ambos pilotos.")

        st.markdown("---")

        # Radios del equipo
        with st.expander("📻 Radios del equipo"):
            radios = obtener_radios(session_key)
            if radios:
                radios_por_piloto = {}
                for radio in radios:
                    num = radio.get("driver_number")
                    if num not in radios_por_piloto:
                        radios_por_piloto[num] = []
                    radios_por_piloto[num].append(radio)

                pilotos_con_radio = []
                for num in radios_por_piloto:
                    piloto_info = pilotos_dict.get(num, {})
                    nombre_p = piloto_info.get("full_name", f"#{num}")
                    n_clips = len(radios_por_piloto[num])
                    pilotos_con_radio.append((f"{nombre_p} ({n_clips} clips)", num))
                pilotos_con_radio.sort(key=lambda x: x[0])

                col_radio1, _ = st.columns([2, 1])
                with col_radio1:
                    piloto_radio_sel = st.selectbox(
                        "Piloto", [p[0] for p in pilotos_con_radio], key="radio_piloto"
                    )
                num_radio_sel = next(
                    (num for nombre, num in pilotos_con_radio if nombre == piloto_radio_sel),
                    None
                )

                if num_radio_sel:
                    clips = radios_por_piloto.get(num_radio_sel, [])
                    clips_ordenados = sorted(clips, key=lambda x: x.get("date", ""), reverse=True)
                    for i, clip in enumerate(clips_ordenados[:5]):
                        url_mp3 = clip.get("recording_url", "")
                        fecha_raw = clip.get("date", "")
                        try:
                            from datetime import datetime, timezone
                            t = datetime.fromisoformat(fecha_raw.replace("Z", "+00:00"))
                            hora_str = t.strftime("%H:%M:%S")
                        except:
                            hora_str = fecha_raw[:19] if fecha_raw else "—"

                        st.markdown(f"**Radio {i+1}** — {hora_str} UTC")
                        if url_mp3:
                            try:
                                resp_audio = requests.get(url_mp3, timeout=10)
                                if resp_audio.status_code == 200:
                                    st.audio(resp_audio.content, format="audio/mp3")
                                else:
                                    st.caption(f"[Escuchar radio]({url_mp3})")
                            except:
                                st.caption(f"[Escuchar radio]({url_mp3})")

                            if st.button(f"Transcribir y analizar clip {i+1}", key=f"transcribe_{i}"):
                                with st.spinner("Transcribiendo con Groq Whisper..."):
                                    try:
                                        resp_audio = requests.get(url_mp3, timeout=15)
                                        if resp_audio.status_code == 200:
                                            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                                                tmp.write(resp_audio.content)
                                                tmp_path = tmp.name
                                            with open(tmp_path, "rb") as audio_file:
                                                transcripcion = cliente.audio.transcriptions.create(
                                                    file=(os.path.basename(tmp_path), audio_file, "audio/mp3"),
                                                    model="whisper-large-v3",
                                                    language="en",
                                                    response_format="text"
                                                )
                                            os.unlink(tmp_path)
                                            resultado = transcripcion.strip() if isinstance(transcripcion, str) else str(transcripcion)
                                            if resultado:
                                                st.info(f"📝 **Transcripción:** {resultado}")
                                                nombre_piloto_radio = piloto_radio_sel.split(' (')[0]
                                                prompt_radio = f"""Eres un comentarista de F1. Esta es la transcripción de una radio de equipo de {nombre_piloto_radio} durante el {nombre_oficial} ({nombre_sesion}): '{resultado}'. Explica en 1-2 frases el contexto y qué significa para la carrera. Habla en español."""
                                                resp_ia = cliente.chat.completions.create(
                                                    model="llama-3.3-70b-versatile",
                                                    messages=[{"role": "user", "content": prompt_radio}],
                                                    max_tokens=200
                                                )
                                                st.success(resp_ia.choices[0].message.content)
                                            else:
                                                st.warning("No se pudo transcribir el audio.")
                                    except Exception as e:
                                        st.error(f"Error al transcribir: {e}")
                        st.markdown("---")
            else:
                st.info(
                    "Las radios del equipo se publican en OpenF1 tras finalizar la sesión. "
                    "Durante la sesión en directo, los clips aparecen con un pequeño retraso. "
                    "Si la sesión acaba de terminar, vuelve a intentarlo en unos minutos."
                )

        st.markdown("---")

        # Documentos FIA F1
        with st.expander("📋 Documentos FIA", expanded=False):
            with st.spinner("Cargando documentos FIA..."):
                docs_f1 = obtener_docs_fia_f1(nombre_carrera)

            if docs_f1:
                st.caption(f"📂 {len(docs_f1)} documentos disponibles para el evento activo")

                # Filtros
                tipos_disponibles = list(set(d['tipo'] for d in docs_f1))
                col_f1, col_f2 = st.columns([3, 1])
                with col_f1:
                    filtro_tipo = st.multiselect(
                        "Filtrar por tipo",
                        options=['decision', 'classification', 'technical', 'note', 'general'],
                        default=['decision', 'classification', 'note'],
                        format_func=lambda x: {'decision': '⚖️ Decisiones', 'classification': '🏁 Clasificaciones', 'technical': '🔧 Técnicos', 'note': '📋 Notas', 'general': '📄 General'}.get(x, x),
                        key="filtro_docs_f1"
                    )

                docs_filtrados = [d for d in docs_f1 if d['tipo'] in filtro_tipo] if filtro_tipo else docs_f1

                for doc in docs_filtrados[:20]:
                    icono = _icono_tipo_doc(doc['tipo'])
                    css_class = f"doc-{doc['tipo']}" if doc['tipo'] in ['decision', 'classification', 'technical'] else ""
                    col_d1, col_d2, col_d3 = st.columns([5, 1, 1])
                    with col_d1:
                        st.markdown(f"{icono} **{doc['titulo']}**")
                    with col_d2:
                        st.markdown(f"[📥 PDF]({doc['url']})")
                    with col_d3:
                        if st.button("🤖 IA", key=f"ia_f1_{doc['titulo'][:20]}"):
                            with st.spinner("Analizando documento..."):
                                analisis = analizar_pdf_con_groq(doc['url'], doc['titulo'], nombre_oficial)
                                st.info(analisis)
                    st.markdown("---")
            else:
                st.info(
                    "Los documentos FIA se cargan desde fia.com. "
                    "Si no aparecen, puede que el sitio esté temporalmente no disponible. "
                    f"Puedes acceder directamente en: [fia.com/documents](https://www.fia.com/documents/championships/fia-formula-one-world-championship-14/)"
                )

        st.markdown("---")

        # Ingeniero de Carrera IA
        st.subheader("Ingeniero de Carrera IA")
        if st.button("⚡ Analizar sesión"):
            resumen_datos = []
            for entrada in clasificacion[:20]:
                numero = entrada.get("driver_number")
                piloto_info = pilotos_dict.get(numero, {})
                nombre = piloto_info.get("full_name", f"Piloto #{numero}")
                equipo = piloto_info.get("team_name", "—")
                posicion = entrada.get("position", "—")
                mejor_vuelta = mejores_vueltas.get(numero)
                tiempo_str = formato_tiempo(mejor_vuelta)
                resumen_datos.append(f"P{posicion}: {nombre} ({equipo}) — Mejor vuelta: {tiempo_str}")

            prompt = f"""Eres un ingeniero de carrera experto de Fórmula 1. Acabas de ver los datos de la sesión {nombre_sesion} del {nombre_oficial}. Clasificación:\n{chr(10).join(resumen_datos)}\nAnaliza en 4-5 frases con pasión y criterio técnico. Habla en español."""
            with st.spinner("El ingeniero está analizando la sesión..."):
                respuesta = cliente.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024
                )
                st.success(respuesta.choices[0].message.content)

    else:
        st.warning("No se pudo cargar la sesión. Comprueba tu conexión.")


# ══════════════════════════════════════════════════════════════════════════════
# ── BLOQUE FORMULA E ──────────────────────────────════════════════════════════
# ══════════════════════════════════════════════════════════════════════════════

elif categoria == "Formula E":

    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Obtener estado de sesión
    status_fe = obtener_estado_sesion_fe()
    is_live = status_fe.get("isLive", False)

    current_race = status_fe.get("currentRaceDetails", {})
    next_race = status_fe.get("nextRaceDetails", {})

    if current_race.get("hasraceresults", False) and next_race:
        active_race = next_race
    else:
        active_race = current_race

    # IDs dinámicos desde la API
    champ_info = obtener_championship_info_fe()
    if champ_info and champ_info.get("championship_id"):
        championship_id = champ_info.get("championship_id")
        event_id = champ_info.get("event_id")
    else:
        # Fallback: usar los IDs del módulo pilotos_fe si existen
        try:
            from pilotos_fe import CHAMPIONSHIP_ID, EVENT_ID_BERLIN
            championship_id = CHAMPIONSHIP_ID
            event_id = EVENT_ID_BERLIN
        except:
            championship_id = ""
            event_id = ""

    nombre_evento = active_race.get("racename", "E-Prix 2026")
    ciudad = active_race.get("city", "Berlin")

    # Cabecera
    if is_live:
        st.markdown('<span style="background:rgba(0,180,255,0.2);border:1px solid rgba(0,180,255,0.5);color:#00b4ff;padding:4px 12px;border-radius:20px;font-weight:700;font-size:0.8rem;">● EN DIRECTO</span>', unsafe_allow_html=True)
        st.markdown("")

    st.subheader(f"⚡ {nombre_evento}")

    features = obtener_feature_info_fe()

    col_live1, col_live2 = st.columns([1, 3])
    with col_live1:
        modo_directo_fe = st.toggle("Modo en directo", key="live_fe")
    with col_live2:
        if modo_directo_fe:
            st.caption("Refrescando cada 30 segundos automáticamente.")

    standings = obtener_standings_fe()
    mejores_vueltas_fe = obtener_mejores_vueltas_fe(championship_id, event_id) if championship_id else {}
    sectores_fe = obtener_sectores_fe(championship_id, event_id) if championship_id else {}
    finishline_data = obtener_finishline_fe(championship_id, event_id) if championship_id else []

    # ── ESTADO DE SESIÓN Y MAPA ───────────────────────────────────────────────
    st.markdown("### Estado de la sesión")
    col_s1, col_s2, col_s3, col_s4 = st.columns([1, 1, 1, 1])

    with col_s1:
        if is_live:
            st.markdown('<span class="flag-badge flag-green">● Sesión activa</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="flag-badge" style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.5);">Sin sesión activa</span>', unsafe_allow_html=True)

    with col_s2:
        if standings:
            estados = set(v.get("status", "") for v in standings.values())
            if "CLASSIFIED" in estados and len(estados) == 1:
                st.markdown(render_flag_badge("CHEQUERED"), unsafe_allow_html=True)
            elif standings:
                st.markdown(render_flag_badge("GREEN FLAG"), unsafe_allow_html=True)
        else:
            st.markdown('<span class="flag-badge" style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.4);">Sin datos</span>', unsafe_allow_html=True)

    with col_s3:
        laps = active_race.get("laps", "—")
        st.metric("Vueltas programadas", laps)

    with col_s4:
        # Mapa del circuito dinámico
        ciudad_upper = ciudad.upper() if ciudad else ""
        TRACK_MAPS = {
            "MEXICO": "https://stats-centre.fiaformulae.com/prod/rc-assets/images/mexico_track.svg",
            "MIAMI": "https://stats-centre.fiaformulae.com/prod/rc-assets/images/miami_track.svg",
            "BERLIN": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Berlin_ePrix_circuit_map.svg/400px-Berlin_ePrix_circuit_map.svg.png",
            "TEMPELHOF": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Berlin_ePrix_circuit_map.svg/400px-Berlin_ePrix_circuit_map.svg.png",
            "MONACO": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Circuit_Monaco.svg/400px-Circuit_Monaco.svg.png",
            "JEDDAH": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Jeddah_Street_Circuit.svg/400px-Jeddah_Street_Circuit.svg.png",
            "SAO PAULO": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Sambadrome_circuit.svg/400px-Sambadrome_circuit.svg.png",
            "MADRID": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/IFEMA_Madrid_circuit.svg/400px-IFEMA_Madrid_circuit.svg.png",
        }
        mapa_url = None
        for key, url in TRACK_MAPS.items():
            if key in ciudad_upper:
                mapa_url = url
                break

        if mapa_url:
            st.image(mapa_url, caption=f"Circuito — {ciudad}", use_container_width=True)
        else:
            st.info(f"📍 {active_race.get('circuitname', ciudad)}")

    st.markdown("---")

    # ── LIVE STREAM (RACE CENTRE EMBED) ───────────────────────────────────────
    with st.expander("📺 Live Stream / Race Centre Oficial", expanded=is_live):
        st.markdown("""
        <iframe src="https://www.fiaformulae.com/en/race-centre" width="100%" height="600" style="border:1px solid rgba(255,255,255,0.1); border-radius:12px;"></iframe>
        """, unsafe_allow_html=True)
        st.caption("El streaming de video en directo depende de los derechos de transmisión en tu país. Si no está disponible, verás el Race Centre oficial.")

    st.markdown("---")

    # ── CLASIFICACIÓN EN TIEMPO REAL ──────────────────────────────────────────
    if standings:
        st.subheader("Clasificación en tiempo real")

        col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 2, 2, 2])
        col1.markdown("**Pos**")
        col2.markdown("**Piloto**")
        col3.markdown("**Equipo**")
        col4.markdown("**Gap**")
        col5.markdown("**Mejor vuelta**")
        col6.markdown("**Cambio pos.**")

        for pos_key in sorted(standings.keys(), key=lambda x: int(x)):
            entrada = standings[pos_key]
            participante = str(entrada.get("participant", ""))
            piloto_info = PILOTOS_FE.get(participante, {"nombre": f"#{participante}", "equipo": "—"})
            posicion = entrada.get("position", "—")
            gap = entrada.get("gapFirstTime", 0)
            cambio = entrada.get("positionChange", 0)
            mejor_vuelta = mejores_vueltas_fe.get(participante, {}).get("best_lap_time")

            gap_str = "Líder" if posicion == 1 else f"+{gap/1000:.3f}s" if gap else "—"
            tiempo_str = ms_a_tiempo(mejor_vuelta)
            cambio_str = f"▲{cambio}" if cambio > 0 else f"▼{abs(cambio)}" if cambio < 0 else "—"

            # Colores por posición igual que F1
            if posicion == 1:
                poscolor = "#ffd700"; posbg = "rgba(255,215,0,0.15)"
            elif posicion == 2:
                poscolor = "#c0c0c0"; posbg = "rgba(192,192,192,0.10)"
            elif posicion == 3:
                poscolor = "#cd7f32"; posbg = "rgba(205,127,50,0.10)"
            else:
                poscolor = "rgba(255,255,255,0.8)"; posbg = "rgba(255,255,255,0.03)"

            col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 2, 2, 2])
            col1.markdown(f'<div style="background:{posbg};border-radius:6px;padding:6px 10px;text-align:center;font-weight:800;color:{poscolor};font-size:1rem">{posicion}</div>', unsafe_allow_html=True)
            col2.markdown(f'<div style="padding:6px 4px;font-weight:700;color:#ffffff">{piloto_info["nombre"]}</div>', unsafe_allow_html=True)
            col3.markdown(f'<div style="padding:6px 4px;color:rgba(255,255,255,0.65);font-size:0.9rem">{piloto_info["equipo"]}</div>', unsafe_allow_html=True)
            col4.markdown(f'<div style="padding:6px 4px;color:rgba(255,255,255,0.85);font-size:0.9rem">{gap_str}</div>', unsafe_allow_html=True)
            col5.markdown(f'<div style="padding:6px 4px;font-family:monospace;color:rgba(255,255,255,0.85);font-size:0.9rem">{tiempo_str}</div>', unsafe_allow_html=True)
            col6.markdown(f'<div style="padding:6px 4px;color:rgba(255,255,255,0.85);font-size:0.9rem">{cambio_str}</div>', unsafe_allow_html=True)

        st.markdown("---")
    # ── RESULTADOS POR SESIÓN ─────────────────────────────────────────────────
    if finishline_data:
        st.subheader("Resultados por sesión")
        nombres_sesiones = [s.get("name", s.get("short_name", "Sesión")) for s in finishline_data]
        if nombres_sesiones:
            tabs = st.tabs(nombres_sesiones)
            for i, (tab, sesion_data) in enumerate(zip(tabs, finishline_data)):
                with tab:
                    posiciones_sesion = sesion_data.get("positions", [])
                    if posiciones_sesion:
                        filas_ses = []
                        for p in posiciones_sesion:
                            driver_num = str(p.get("driverNumber", ""))
                            piloto_info = PILOTOS_FE.get(driver_num, {"nombre": f"#{driver_num}", "equipo": "—"})
                            gap_raw = p.get("gap_first_time")
                            gap_str = "Líder" if p.get("position") == 1 else (f"+{int(gap_raw)/1000:.3f}s" if gap_raw else "—")
                            filas_ses.append({
                                "Pos": p.get("position", "—"),
                                "Piloto": piloto_info["nombre"],
                                "Equipo": piloto_info["equipo"],
                                "Gap": gap_str,
                                "Estado": p.get("status", "—"),
                            })
                        st.dataframe(pd.DataFrame(filas_ses), use_container_width=True, hide_index=True)
                    else:
                        st.info("Sin datos para esta sesión.")

        st.markdown("---")

    # ── TIEMPOS POR SECTOR ────────────────────────────────────────────────────
    if sectores_fe:
        st.subheader("Mejores tiempos por sector")
        filas_sec = []
        for num, datos in sectores_fe.items():
            piloto_info = PILOTOS_FE.get(str(num), {"nombre": f"#{num}", "equipo": "—"})
            s1 = datos.get("1")
            s2 = datos.get("2")
            s3 = datos.get("3")
            filas_sec.append({
                "Piloto": piloto_info["nombre"],
                "S1": f"{s1/1000:.3f}s" if s1 else "—",
                "S2": f"{s2/1000:.3f}s" if s2 else "—",
                "S3": f"{s3/1000:.3f}s" if s3 else "—",
            })
        if filas_sec:
            st.dataframe(pd.DataFrame(filas_sec), use_container_width=True, hide_index=True)
        st.markdown("---")

    # ── DOCUMENTOS FIA FORMULA E (DINÁMICO) ───────────────────────────────────
    with st.expander("📋 Documentos FIA Formula E", expanded=False):
        with st.spinner("Cargando documentos FIA Formula E..."):
            eventos_fe = obtener_eventos_fe_docs()

        if eventos_fe:
            # Selector de evento (por defecto el más reciente)
            nombres_eventos = [e[0] for e in eventos_fe]
            evento_sel_nombre = st.selectbox(
                "Evento",
                nombres_eventos,
                index=0,
                key="selector_evento_fe_docs"
            )
            evento_sel_id = next((e[1] for e in eventos_fe if e[0] == evento_sel_nombre), None)

            if evento_sel_id:
                docs_fe = obtener_docs_fe_evento(evento_sel_id)

                if docs_fe:
                    st.caption(f"📂 {len(docs_fe)} documentos disponibles para {evento_sel_nombre}")

                    # Filtros
                    col_f1_fe, _ = st.columns([3, 1])
                    with col_f1_fe:
                        filtro_tipo_fe = st.multiselect(
                            "Filtrar por tipo",
                            options=['decision', 'classification', 'technical', 'note', 'general'],
                            default=['decision', 'classification', 'note'],
                            format_func=lambda x: {'decision': '⚖️ Decisiones', 'classification': '🏁 Clasificaciones', 'technical': '🔧 Técnicos', 'note': '📋 Notas', 'general': '📄 General'}.get(x, x),
                            key="filtro_docs_fe"
                        )

                    docs_filtrados_fe = [d for d in docs_fe if d['tipo'] in filtro_tipo_fe] if filtro_tipo_fe else docs_fe

                    for doc in docs_filtrados_fe:
                        icono = _icono_tipo_doc(doc['tipo'])
                        col_d1, col_d2, col_d3 = st.columns([5, 1, 1])
                        with col_d1:
                            st.markdown(f"{icono} **{doc['titulo']}**")
                        with col_d2:
                            st.markdown(f"[📥 PDF]({doc['url']})")
                        with col_d3:
                            if st.button("🤖 IA", key=f"ia_fe_{doc['titulo'][:25]}"):
                                with st.spinner("Analizando documento..."):
                                    analisis = analizar_pdf_con_groq(doc['url'], doc['titulo'], nombre_evento)
                                    st.info(analisis)
                        st.markdown("---")
                else:
                    st.info(f"No hay documentos disponibles para {evento_sel_nombre}.")
        else:
            st.info(
                "No se pudieron cargar los documentos FIA. "
                "Puedes acceder directamente en: [results.formulae.fia.com/documents](https://results.formulae.fia.com/documents)"
            )

    st.markdown("---")

    # ── NOTA SOBRE ATTACK MODE Y ENERGÍA ─────────────────────────────────────
    with st.expander("ℹ️ Attack Mode y Energía — Estado de integración"):
        st.markdown("""
        **Attack Mode** y **Energía restante** se transmiten a través de Firebase Realtime Database
        (protegida por Firebase AppCheck/reCAPTCHA), por lo que no son accesibles mediante peticiones
        REST directas desde esta app.

        **Lo que sí está disponible:**
        - Posiciones en tiempo real ✅
        - Mejores vueltas por piloto ✅
        - Tiempos por sector ✅
        - Resultados de todas las sesiones (Qualifying, Duelos, FP) ✅
        - Estado de la sesión (activa/inactiva, carrera programada) ✅
        - Documentos FIA de todos los eventos de la temporada ✅
        - Análisis IA de documentos FIA ✅
        - Análisis IA de la sesión ✅
        """)

    # ── INGENIERO DE CARRERA IA ───────────────────────────────────────────────
    st.subheader("Ingeniero de Carrera IA")

    datos_disponibles = standings or finishline_data

    if st.button("Analizar sesión FE"):
        if not datos_disponibles:
            st.warning("No hay datos disponibles para analizar.")
        else:
            resumen_fe = []
            if standings:
                for pos_key in sorted(standings.keys(), key=lambda x: int(x))[:10]:
                    entrada = standings[pos_key]
                    participante = str(entrada.get("participant", ""))
                    piloto_info = PILOTOS_FE.get(participante, {"nombre": f"#{participante}", "equipo": "—"})
                    posicion = entrada.get("position", "—")
                    gap = entrada.get("gapFirstTime", 0)
                    mejor_vuelta = mejores_vueltas_fe.get(participante, {}).get("best_lap_time")
                    gap_str = "Líder" if posicion == 1 else f"+{gap/1000:.3f}s" if gap else "—"
                    tiempo_str = ms_a_tiempo(mejor_vuelta)
                    resumen_fe.append(f"P{posicion}: {piloto_info['nombre']} ({piloto_info['equipo']}) — Gap: {gap_str} — Mejor vuelta: {tiempo_str}")
                contexto_sesion = "clasificación en tiempo real"
            elif finishline_data:
                ultima_sesion = finishline_data[-1]
                nombre_ses = ultima_sesion.get("name", "Sesión")
                for p in ultima_sesion.get("positions", [])[:10]:
                    driver_num = str(p.get("driverNumber", ""))
                    piloto_info = PILOTOS_FE.get(driver_num, {"nombre": f"#{driver_num}", "equipo": "—"})
                    gap_raw = p.get("gap_first_time")
                    gap_str = "Líder" if p.get("position") == 1 else (f"+{int(gap_raw)/1000:.3f}s" if gap_raw else "—")
                    resumen_fe.append(f"P{p.get('position', '—')}: {piloto_info['nombre']} ({piloto_info['equipo']}) — Gap: {gap_str}")
                contexto_sesion = f"resultados de {nombre_ses}"

            datos_fe_texto = "\n".join(resumen_fe)
            prompt_fe = f"""Eres un comentarista experto de Formula E con conocimiento técnico profundo del campeonato.
Estos son los datos del {nombre_evento} ({contexto_sesion}):

{datos_fe_texto}

Genera un análisis apasionado y técnico en 4-5 frases. Menciona la batalla por el liderato,
los gaps entre pilotos, quién parece tener mejor ritmo y qué puede pasar en la carrera.
Habla en español, con el tono de un comentarista experto de Eurosport."""

            with st.spinner("Analizando sesión de Formula E..."):
                respuesta_fe = cliente.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt_fe}],
                    max_tokens=600
                )
                st.success(respuesta_fe.choices[0].message.content)

    if not datos_disponibles:
        st.info("No hay datos en tiempo real disponibles. La sesión puede no estar activa.")
        if active_race:
            start_time = active_race.get("start_time", "")
            if start_time:
                st.markdown(f"**Hora de inicio programada:** {start_time}")

    if modo_directo_fe:
        time.sleep(30)
        st.rerun()
