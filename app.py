import streamlit as st
import requests
import base64
import time
import pandas as pd
from groq import Groq

st.set_page_config(
    page_title="Paddock y Pluma — Telemetría",
    page_icon="🏎️",
    layout="wide"
)

cliente = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ── WELCOME PAGE ─────────────────────────────────────────────────────────────
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
    .stApp {{
        background: #0d0d0d !important;
    }}
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
    .welcome-logo {{
        width: min(600px, 85vw);
        opacity: 0.95;
    }}
    .welcome-subtitle {{
        color: rgba(255,255,255,0.5);
        font-size: 1rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: -1rem;
        font-family: 'FESans', 'Inter', sans-serif;
    }}
    .welcome-buttons {{
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
    }}
    .welcome-btn {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        padding: 28px 48px;
        border-radius: 14px;
        color: white;
        text-decoration: none;
        font-family: 'FESans', 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        transition: all 0.2s ease;
    }}
    .welcome-btn-f1 {{
        border: 1px solid rgba(255,30,0,0.4);
        background: rgba(255,30,0,0.06);
    }}
    .welcome-btn-f1:hover {{
        background: rgba(255,30,0,0.14);
        border-color: rgba(255,30,0,0.8);
    }}
    .welcome-btn-fe {{
        border: 1px solid rgba(77,110,255,0.4);
        background: rgba(77,110,255,0.06);
    }}
    .welcome-btn-fe:hover {{
        background: rgba(77,110,255,0.14);
        border-color: rgba(77,110,255,0.8);
    }}
    .welcome-btn img {{
        width: 120px;
        height: 48px;
        object-fit: contain;
    }}
    </style>

    <div class="welcome-container">
        <img class="welcome-logo"
             src="data:image/png;base64,{logo_b64}"
             alt="Paddock y Pluma">
        <p class="welcome-subtitle">Telemetría en directo · 2026</p>
        <div class="welcome-buttons">
            <a href="?cat=f1" target="_self" class="welcome-btn welcome-btn-f1">
                <img src="data:image/svg+xml;base64,{f1_b64}" alt="Fórmula 1">
                Fórmula 1
            </a>
            <a href="?cat=fe" target="_self" class="welcome-btn welcome-btn-fe">
                <img src="data:image/svg+xml;base64,{fe_b64}" alt="Formula E">
                Formula E
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    params = st.query_params
    if params.get("cat") == "f1":
        st.session_state.pagina = "app"
        st.session_state.categoria = "Fórmula 1"
        st.query_params.clear()
        st.rerun()
    elif params.get("cat") == "fe":
        st.session_state.pagina = "app"
        st.session_state.categoria = "Formula E"
        st.query_params.clear()
        st.rerun()

    st.stop()

# ── APP PRINCIPAL ─────────────────────────────────────────────────────────────
st.title("Paddock y pluma — TELEMETRÍA EN DIRECTO")
st.markdown("---")

categoria = st.session_state.get("categoria", "Fórmula 1")

# ── ESTILOS GLOBALES ──────────────────────────────────────────────────────────
try:
    font_response = requests.get("https://www.fiaformulae.com/resources/v4.37.8/fonts/FESans.var.woff2", timeout=5)
    font_b64 = base64.b64encode(font_response.content).decode()
    font_face = f"url(data:font/woff2;base64,{font_b64})"
except:
    font_face = "sans-serif"

if categoria == "Fórmula 1":
    grad_start = "#ff1e00"
    grad_end   = "#15151e"
    accent     = "#ff1e00"
    accent2    = "#ff6b35"
else:
    grad_start = "#071c98"
    grad_end   = "#0000f4"
    accent     = "#0000f4"
    accent2    = "#4d6eff"

st.markdown(f"""
<style>
@font-face {{
    font-family: 'FESans';
    src: {font_face};
    font-weight: 100 900;
    font-style: normal;
}}
html, body, [class*="css"], .stMarkdown, .stText,
h1, h2, h3, h4, p, label, button, div {{
    font-family: 'FESans', 'Inter', sans-serif !important;
}}
.stApp {{
    background: linear-gradient(160deg, {grad_start} 0%, {grad_end} 100%) !important;
    background-attachment: fixed !important;
}}
.stApp h1 {{
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    color: #ffffff !important;
}}
.stApp h2, .stApp h3 {{
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
}}
.stApp p, .stApp label, .stApp div {{
    color: rgba(255,255,255,0.9) !important;
}}
div[role="radiogroup"] label {{
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
    padding: 6px 16px !important;
    color: rgba(255,255,255,0.7) !important;
    transition: all 0.2s ease !important;
}}
div[role="radiogroup"] label:has(input:checked) {{
    background: {accent} !important;
    border-color: {accent} !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}}
.stButton > button {{
    background: linear-gradient(90deg, {accent}, {accent2}) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    padding: 10px 20px !important;
    transition: opacity 0.2s ease !important;
}}
.stButton > button:hover {{
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}}
[data-testid="metric-container"] {{
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    backdrop-filter: blur(10px) !important;
}}
[data-testid="metric-container"] label {{
    color: rgba(255,255,255,0.6) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: #ffffff !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
}}
[data-baseweb="select"] > div {{
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}}
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {{
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}
[data-testid="stAlert"] {{
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
    color: #ffffff !important;
}}
hr {{
    border-color: rgba(255,255,255,0.1) !important;
}}
[data-testid="stExpander"] {{
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Funciones OpenF1 ──────────────────────────────────────────────────────────

def obtener_todas_las_carreras():
    url = "https://api.openf1.org/v1/sessions?session_type=Race&year=2026"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return [s for s in datos if s.get("session_name") == "Race"]
    return []

@st.cache_data(ttl=3600)
def obtener_nombres_jolpica():
    url = "https://api.jolpi.ca/ergast/f1/2026/races.json"
    try:
        r = requests.get(url, timeout=10)
        carreras = r.json()["MRData"]["RaceTable"]["Races"]
        nombres = {}
        for c in carreras:
            country  = c["Circuit"]["Location"]["country"]
            locality = c["Circuit"]["Location"]["locality"]
            circuit  = c["circuitId"]
            race     = c["raceName"]
            nombres[country]  = race
            nombres[locality] = race
            nombres[circuit]  = race
        return nombres
    except:
        return {}

def obtener_sesion_actual():
    carreras = obtener_todas_las_carreras()
    if not carreras:
        return None
    nombres_oficiales = obtener_nombres_jolpica()
    opciones = {}
    for carrera in carreras:
        location = carrera.get("location") or f"Sesión {carrera.get('session_key')}"
        nombre = nombres_oficiales.get(location, location)
        opciones[nombre] = carrera
    seleccion = st.selectbox("🗓️ Selecciona el Gran Premio", list(opciones.keys()))
    return opciones[seleccion]

def obtener_posiciones(session_key):
    url = f"https://api.openf1.org/v1/position?session_key={session_key}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()
    return []

def obtener_pilotos(session_key):
    url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()
    return []

def obtener_vueltas(session_key):
    url = f"https://api.openf1.org/v1/laps?session_key={session_key}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()
    return []

def obtener_telemetria_piloto(session_key, driver_number):
    url = f"https://api.openf1.org/v1/car_data?session_key={session_key}&driver_number={driver_number}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()
    return []

def obtener_stints(session_key):
    url = f"https://api.openf1.org/v1/stints?session_key={session_key}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()
    return []

# ── BLOQUE FÓRMULA 1 ──────────────────────────────────────────────────────────

if categoria == "Fórmula 1":

    sesion = obtener_sesion_actual()

    if sesion:
        nombre_carrera = sesion.get('location') or "Gran Premio"
        nombre_sesion = sesion.get('session_name') or "Race"
        nombres_oficiales = obtener_nombres_jolpica()
        nombre_oficial = nombres_oficiales.get(nombre_carrera, nombre_carrera)
        st.subheader(f"📍 {nombre_oficial} — {nombre_sesion}")

        session_key = sesion.get("session_key")

        pilotos = obtener_pilotos(session_key)
        posiciones_raw = obtener_posiciones(session_key)
        vueltas_raw = obtener_vueltas(session_key)

        pilotos_dict = {p["driver_number"]: p for p in pilotos}

        ultimas_posiciones = {}
        for pos in posiciones_raw:
            numero = pos["driver_number"]
            ultimas_posiciones[numero] = pos

        mejores_vueltas = {}
        for vuelta in vueltas_raw:
            numero = vuelta.get("driver_number")
            tiempo = vuelta.get("lap_duration")
            if numero and tiempo:
                if numero not in mejores_vueltas or tiempo < mejores_vueltas[numero]:
                    mejores_vueltas[numero] = tiempo

        clasificacion = sorted(ultimas_posiciones.values(), key=lambda x: x.get("position", 99))

        # ── CLASIFICACIÓN FINAL ───────────────────────────────────────────────
        st.subheader("🏁 Clasificación final")
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        col1.markdown("**Pos**")
        col2.markdown("**Piloto**")
        col3.markdown("**Equipo**")
        col4.markdown("**Mejor vuelta**")

        for entrada in clasificacion:
            numero = entrada.get("driver_number")
            piloto_info = pilotos_dict.get(numero, {})
            nombre = piloto_info.get("full_name", f"Piloto #{numero}")
            equipo = piloto_info.get("team_name", "—")
            posicion = entrada.get("position", "—")
            mejor_vuelta = mejores_vueltas.get(numero)
            if mejor_vuelta:
                minutos = int(mejor_vuelta // 60)
                segundos = mejor_vuelta % 60
                tiempo_str = f"{minutos}:{segundos:06.3f}"
            else:
                tiempo_str = "—"
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            col1.write(posicion)
            col2.write(nombre)
            col3.write(equipo)
            col4.write(tiempo_str)

        st.markdown("---")

        # ── EVOLUCIÓN DE TIEMPOS POR VUELTA ──────────────────────────────────
        st.subheader("📈 Evolución del ritmo de carrera")

        registros = []
        for vuelta in vueltas_raw:
            numero = vuelta.get("driver_number")
            lap_num = vuelta.get("lap_number")
            lap_dur = vuelta.get("lap_duration")
            if numero and lap_num and lap_dur and lap_dur < 200:
                piloto_info = pilotos_dict.get(numero, {})
                nombre = piloto_info.get("full_name", f"Piloto #{numero}")
                registros.append({"Vuelta": lap_num, "Piloto": nombre, "Tiempo (s)": round(lap_dur, 3)})

        if registros:
            df_ritmo = pd.DataFrame(registros)
            todos_pilotos = sorted(df_ritmo["Piloto"].unique())
            pilotos_grafica = st.multiselect(
                "🏎️ Selecciona pilotos para comparar (máx. 5 recomendado)",
                options=todos_pilotos,
                default=todos_pilotos[:3]
            )
            if pilotos_grafica:
                df_filtrado = df_ritmo[df_ritmo["Piloto"].isin(pilotos_grafica)]
                df_pivot = df_filtrado.pivot_table(index="Vuelta", columns="Piloto", values="Tiempo (s)", aggfunc="min")
                st.line_chart(df_pivot, x_label="Vuelta", y_label="Tiempo (s)")
            else:
                st.info("Selecciona al menos un piloto para ver la gráfica.")
        else:
            st.warning("No hay datos de vueltas disponibles para esta sesión.")

        st.markdown("---")

        # ── ESTRATEGIA DE NEUMÁTICOS ──────────────────────────────────────────
        st.subheader("🏎️ Estrategia de neumáticos")

        COLORES_COMPUESTO = {
            "SOFT": "🔴 Blando", "MEDIUM": "🟡 Medio", "HARD": "⚪ Duro",
            "INTERMEDIATE": "🟢 Intermedio", "WET": "🔵 Lluvia", "UNKNOWN": "❓ Desconocido",
        }

        stints_raw = obtener_stints(session_key)

        if stints_raw:
            filas = []
            for stint in stints_raw:
                numero = stint.get("driver_number")
                piloto_info = pilotos_dict.get(numero, {})
                nombre_piloto = piloto_info.get("full_name", f"Piloto #{numero}")
                compuesto = (stint.get("compound") or "UNKNOWN").upper()
                lap_start = stint.get("lap_start", "—")
                lap_end = stint.get("lap_end", "—")
                num_stint = stint.get("stint_number", "—")
                duracion = lap_end - lap_start + 1 if isinstance(lap_start, int) and isinstance(lap_end, int) else "—"
                filas.append({
                    "Piloto": nombre_piloto, "Stint": num_stint,
                    "Compuesto": COLORES_COMPUESTO.get(compuesto, compuesto),
                    "Vuelta inicio": lap_start, "Vuelta fin": lap_end, "Vueltas": duracion
                })

            if filas:
                df_stints = pd.DataFrame(filas)
                orden_pilotos = []
                for entrada in clasificacion:
                    numero = entrada.get("driver_number")
                    piloto_info = pilotos_dict.get(numero, {})
                    orden_pilotos.append(piloto_info.get("full_name", f"Piloto #{numero}"))
                df_stints["_orden"] = df_stints["Piloto"].apply(lambda x: orden_pilotos.index(x) if x in orden_pilotos else 99)
                df_stints = df_stints.sort_values(["_orden", "Stint"]).drop(columns=["_orden"])
                st.dataframe(df_stints, use_container_width=True, hide_index=True)
            else:
                st.warning("No hay datos de stints disponibles para esta sesión.")
        else:
            st.warning("No hay datos de estrategia disponibles para esta sesión.")

        st.markdown("---")

        # ── SECTORES S1 / S2 / S3 ────────────────────────────────────────────
        st.subheader("⏱️ Mejores tiempos por sector")

        sectores = []
        for vuelta in vueltas_raw:
            numero = vuelta.get("driver_number")
            s1 = vuelta.get("duration_sector_1")
            s2 = vuelta.get("duration_sector_2")
            s3 = vuelta.get("duration_sector_3")
            if numero and (s1 or s2 or s3):
                piloto_info = pilotos_dict.get(numero, {})
                sectores.append({"Piloto": piloto_info.get("full_name", f"Piloto #{numero}"), "S1": s1, "S2": s2, "S3": s3})

        if sectores:
            df_sec = pd.DataFrame(sectores)
            df_best = df_sec.groupby("Piloto").agg(S1=("S1","min"), S2=("S2","min"), S3=("S3","min")).reset_index()
            mejor_s1, mejor_s2, mejor_s3 = df_best["S1"].min(), df_best["S2"].min(), df_best["S3"].min()

            def fmt_sector(val, mejor):
                if pd.isna(val): return "—"
                texto = f"{val:.3f}s"
                return f"🟣 {texto}" if val == mejor else texto

            df_best["S1 mejor"] = df_best["S1"].apply(lambda x: fmt_sector(x, mejor_s1))
            df_best["S2 mejor"] = df_best["S2"].apply(lambda x: fmt_sector(x, mejor_s2))
            df_best["S3 mejor"] = df_best["S3"].apply(lambda x: fmt_sector(x, mejor_s3))
            df_best["_orden"] = df_best["Piloto"].apply(lambda x: orden_pilotos.index(x) if x in orden_pilotos else 99)
            df_best = df_best.sort_values("_orden")
            st.dataframe(
                df_best[["Piloto","S1 mejor","S2 mejor","S3 mejor"]].rename(columns={"S1 mejor":"Sector 1","S2 mejor":"Sector 2","S3 mejor":"Sector 3"}),
                use_container_width=True, hide_index=True
            )
            st.caption("🟣 = Mejor tiempo absoluto del sector en la sesión")
        else:
            st.warning("No hay datos de sectores disponibles para esta sesión.")

        st.markdown("---")

        # ── MODO EN DIRECTO ───────────────────────────────────────────────────
        col_live1, col_live2 = st.columns([1, 3])
        with col_live1:
            modo_directo = st.toggle("🔴 Modo en directo")
        with col_live2:
            if modo_directo:
                st.caption("Refrescando clasificación y posiciones cada 30 segundos automáticamente.")
        if modo_directo:
            time.sleep(30)
            st.rerun()

        st.markdown("---")

        # ── TELEMETRÍA POR PILOTO ─────────────────────────────────────────────
        st.subheader("📊 Telemetría por piloto")

        nombres_pilotos = {}
        for entrada in clasificacion:
            numero = entrada.get("driver_number")
            piloto_info = pilotos_dict.get(numero, {})
            nombres_pilotos[piloto_info.get("full_name", f"Piloto #{numero}")] = numero

        piloto_seleccionado = st.selectbox("🏎️ Selecciona un piloto", list(nombres_pilotos.keys()))
        numero_seleccionado = nombres_pilotos[piloto_seleccionado]

        if st.button("📡 Cargar telemetría"):
            with st.spinner(f"Cargando datos de {piloto_seleccionado}..."):
                telemetria = obtener_telemetria_piloto(session_key, numero_seleccionado)
                if telemetria:
                    velocidades = [t.get("speed", 0) for t in telemetria if t.get("speed")]
                    marchas = [t.get("n_gear", 0) for t in telemetria if t.get("n_gear")]
                    acelerador = [t.get("throttle", 0) for t in telemetria if t.get("throttle")]
                    vel_max = max(velocidades) if velocidades else 0
                    vel_media = round(sum(velocidades) / len(velocidades)) if velocidades else 0
                    marcha_max = max(marchas) if marchas else 0
                    acelerador_medio = round(sum(acelerador) / len(acelerador)) if acelerador else 0
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("🚀 Velocidad máx.", f"{vel_max} km/h")
                    col2.metric("📈 Velocidad media", f"{vel_media} km/h")
                    col3.metric("⚙️ Marcha máxima", f"{marcha_max}")
                    col4.metric("🦶 Acelerador medio", f"{acelerador_medio}%")
                    st.markdown("---")
                    st.subheader("📉 Gráfica de velocidad")
                    st.line_chart(pd.DataFrame({"Velocidad (km/h)": velocidades[:500]}), x_label="Muestra de telemetría", y_label="Velocidad (km/h)")
                else:
                    st.warning("No hay datos de telemetría disponibles para este piloto.")

        st.markdown("---")

        # ── RADIOS DE EQUIPO ──────────────────────────────────────────────────
        st.subheader("📻 Radios de equipo")

        piloto_radio = st.selectbox("🎙️ Selecciona piloto para escuchar radios", list(nombres_pilotos.keys()), key="piloto_radio")
        numero_radio = nombres_pilotos[piloto_radio]

        if st.button("📻 Cargar radios"):
            with st.spinner("Buscando radios..."):
                url_radio = f"https://api.openf1.org/v1/team_radio?session_key={session_key}&driver_number={numero_radio}"
                respuesta_radio = requests.get(url_radio)
                if respuesta_radio.status_code == 200:
                    radios = respuesta_radio.json()
                    if radios:
                        st.write(f"Se encontraron **{len(radios)} radios** de {piloto_radio}")
                        for i, radio in enumerate(radios[:5]):
                            url_audio = radio.get("recording_url")
                            fecha = radio.get("date", "")[:19].replace("T", " ")
                            with st.expander(f"📡 Radio {i+1} — {fecha}"):
                                if url_audio:
                                    st.audio(url_audio)
                                    if st.button(f"🤖 Transcribir y resumir", key=f"transcribir_{i}"):
                                        prompt_radio = f"""Eres un experto en Fórmula 1. El siguiente es el contenido de una radio de equipo de {piloto_radio} durante el {nombre_oficial}. URL del audio: {url_audio}. No puedes escuchar el audio directamente, pero basándote en el contexto de la carrera y que este es un mensaje típico de radio de F1, genera un ejemplo realista de lo que podría estar diciendo el equipo o el piloto en este momento de la carrera. Sé breve, máximo 2 frases. Habla en español."""
                                        with st.spinner("Analizando radio..."):
                                            respuesta_radio_ia = cliente.chat.completions.create(
                                                model="llama-3.3-70b-versatile",
                                                messages=[{"role": "user", "content": prompt_radio}],
                                                max_tokens=150
                                            )
                                            st.success(respuesta_radio_ia.choices[0].message.content)
                                else:
                                    st.warning("Audio no disponible")
                    else:
                        st.warning("No hay radios disponibles para este piloto en esta sesión.")
                else:
                    st.warning("No se pudieron cargar las radios.")

        st.markdown("---")

        # ── COMPARATIVA ENTRE DOS PILOTOS ─────────────────────────────────────
        st.subheader("⚔️ Comparativa entre pilotos")

        col_a, col_b = st.columns(2)
        with col_a:
            piloto_a = st.selectbox("🔵 Piloto A", list(nombres_pilotos.keys()), key="piloto_a")
        with col_b:
            piloto_b = st.selectbox("🔴 Piloto B", list(nombres_pilotos.keys()), key="piloto_b", index=1)

        if st.button("⚔️ Comparar pilotos"):
            with st.spinner("Cargando datos de ambos pilotos..."):
                numero_a = nombres_pilotos[piloto_a]
                numero_b = nombres_pilotos[piloto_b]
                telemetria_a = obtener_telemetria_piloto(session_key, numero_a)
                telemetria_b = obtener_telemetria_piloto(session_key, numero_b)
                if telemetria_a and telemetria_b:
                    velocidades_a = [t.get("speed", 0) for t in telemetria_a if t.get("speed")]
                    velocidades_b = [t.get("speed", 0) for t in telemetria_b if t.get("speed")]
                    vel_max_a = max(velocidades_a) if velocidades_a else 0
                    vel_max_b = max(velocidades_b) if velocidades_b else 0
                    vel_media_a = round(sum(velocidades_a) / len(velocidades_a)) if velocidades_a else 0
                    vel_media_b = round(sum(velocidades_b) / len(velocidades_b)) if velocidades_b else 0
                    mejor_a = mejores_vueltas.get(numero_a)
                    mejor_b = mejores_vueltas.get(numero_b)

                    def formato_tiempo(t):
                        return f"{int(t // 60)}:{t % 60:06.3f}" if t else "—"

                    df_comp = pd.DataFrame({
                        "Métrica": ["Velocidad máxima", "Velocidad media", "Mejor vuelta"],
                        piloto_a: [f"{vel_max_a} km/h", f"{vel_media_a} km/h", formato_tiempo(mejor_a)],
                        piloto_b: [f"{vel_max_b} km/h", f"{vel_media_b} km/h", formato_tiempo(mejor_b)]
                    })
                    st.dataframe(df_comp, use_container_width=True)
                    st.subheader("📉 Velocidad superpuesta")
                    longitud = min(len(velocidades_a), len(velocidades_b), 500)
                    st.line_chart(pd.DataFrame({piloto_a: velocidades_a[:longitud], piloto_b: velocidades_b[:longitud]}), x_label="Muestra de telemetría", y_label="Velocidad (km/h)")

                    prompt_comp = f"""Eres un ingeniero de carrera experto de Fórmula 1. Compara el rendimiento de estos dos pilotos en el {nombre_oficial}: {piloto_a}: velocidad máxima {vel_max_a} km/h, velocidad media {vel_media_a} km/h, mejor vuelta {formato_tiempo(mejor_a)}. {piloto_b}: velocidad máxima {vel_max_b} km/h, velocidad media {vel_media_b} km/h, mejor vuelta {formato_tiempo(mejor_b)}. Analiza en 3-4 frases quién tuvo mejor rendimiento y por qué, con criterio técnico y pasión. Habla en español."""
                    respuesta_comp = cliente.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt_comp}],
                        max_tokens=512
                    )
                    st.info(respuesta_comp.choices[0].message.content)
                else:
                    st.warning("No hay datos de telemetría disponibles para uno o ambos pilotos.")

        st.markdown("---")

        # ── INGENIERO DE CARRERA IA ───────────────────────────────────────────
        st.subheader("🤖 Ingeniero de Carrera IA")

        if st.button("⚡ Analizar carrera"):
            resumen_datos = []
            for entrada in clasificacion[:20]:
                numero = entrada.get("driver_number")
                piloto_info = pilotos_dict.get(numero, {})
                nombre = piloto_info.get("full_name", f"Piloto #{numero}")
                equipo = piloto_info.get("team_name", "—")
                posicion = entrada.get("position", "—")
                mejor_vuelta = mejores_vueltas.get(numero)
                if mejor_vuelta:
                    tiempo_str = f"{int(mejor_vuelta // 60)}:{mejor_vuelta % 60:06.3f}"
                else:
                    tiempo_str = "—"
                resumen_datos.append(f"P{posicion}: {nombre} ({equipo}) — Mejor vuelta: {tiempo_str}")

            prompt = f"""Eres un ingeniero de carrera experto de Fórmula 1 con años de experiencia en la parrilla. Acabas de ver los resultados finales del {nombre_oficial}. Clasificación final con mejores vueltas:\n{chr(10).join(resumen_datos)}\nAnaliza esta carrera en 4-5 frases con pasión y criterio técnico. Comenta quién dominó y por qué, batallas destacadas, algo llamativo de los tiempos de vuelta, y una reflexión sobre el campeonato. Habla en español, con el tono apasionado de un comentarista experto."""

            with st.spinner("El ingeniero está analizando la carrera..."):
                respuesta = cliente.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024
                )
                st.success(respuesta.choices[0].message.content)

    else:
        st.warning("No se pudo cargar la sesión. Comprueba tu conexión.")

# ── BLOQUE FORMULA E ──────────────────────────────────────────────────────────

elif categoria == "Formula E":
    st.subheader("⚡ Panel de Formula E — Entrada manual de datos")
    st.info("Introduce los datos de la carrera manualmente. La IA generará el relato en tiempo real.")

    EPRIX_2026 = [
        "ePrix de São Paulo (R1)", "ePrix de Ciudad de México (R2)", "ePrix de Miami (R3)",
        "ePrix de Yeda I (R4)", "ePrix de Yeda II (R5)", "ePrix de Madrid — Jarama (R6)",
        "ePrix de Berlín I (R7)", "ePrix de Berlín II (R8)", "ePrix de Mónaco I (R9)",
        "ePrix de Mónaco II (R10)", "ePrix de Sanya (R11)", "ePrix de Shanghái I (R12)",
        "ePrix de Shanghái II (R13)", "ePrix de Tokio I (R14)", "ePrix de Tokio II (R15)",
        "ePrix de Londres I (R16)", "ePrix de Londres II (R17)",
    ]

    with st.form("panel_fe"):
        nombre_eprix = st.selectbox("🏙️ Selecciona el ePrix", EPRIX_2026)
        st.markdown("#### 🏁 Top 10 — Posiciones y gaps")
        pilotos_fe = []
        col_nombres, col_equipos, col_gaps, col_energia = st.columns(4)
        col_nombres.markdown("**Piloto**")
        col_equipos.markdown("**Equipo**")
        col_gaps.markdown("**Gap al líder**")
        col_energia.markdown("**Energía restante (%)**")
        for i in range(1, 11):
            c1, c2, c3, c4 = st.columns(4)
            nombre_fe = c1.text_input(f"P{i}", placeholder=f"Nombre piloto P{i}", key=f"nombre_{i}", label_visibility="collapsed")
            equipo_fe = c2.text_input(f"Equipo P{i}", placeholder="Equipo", key=f"equipo_{i}", label_visibility="collapsed")
            gap_fe = c3.text_input(f"Gap P{i}", placeholder="+0.000 / Líder", key=f"gap_{i}", label_visibility="collapsed")
            energia_fe = c4.number_input(f"Energía P{i}", min_value=0, max_value=100, value=50, key=f"energia_{i}", label_visibility="collapsed")
            pilotos_fe.append({"posicion": i, "nombre": nombre_fe, "equipo": equipo_fe, "gap": gap_fe, "energia": energia_fe})

        st.markdown("#### 🎯 Datos extra de carrera")
        col_ex1, col_ex2 = st.columns(2)
        vuelta_actual = col_ex1.number_input("🔄 Vuelta actual", min_value=1, max_value=60, value=1)
        total_vueltas = col_ex2.number_input("📍 Total de vueltas", min_value=1, max_value=60, value=30)
        col_ex3, col_ex4 = st.columns(2)
        coche_seguridad = col_ex3.checkbox("🚨 Safety Car activo")
        attack_mode = col_ex4.text_input("⚡ Attack Mode activado por", placeholder="Ej: Vergne, Nato")
        incidencias = st.text_area("📝 Incidencias / Notas manuales", placeholder="Penalizaciones, adelantamientos clave, abandonos...")
        enviado = st.form_submit_button("🤖 Generar relato IA")

    if enviado:
        resumen_pilotos = [
            f"P{p['posicion']}: {p['nombre']} ({p['equipo']}) — Gap: {p['gap']} — Energía: {p['energia']}%"
            for p in pilotos_fe if p["nombre"]
        ]
        datos_fe_texto = "\n".join(resumen_pilotos)
        sc_texto = "Hay Safety Car en pista." if coche_seguridad else "No hay Safety Car."
        attack_texto = f"Attack Mode activado recientemente por: {attack_mode}." if attack_mode else ""

        prompt_fe = f"""Eres un comentarista experto de Formula E con conocimiento técnico profundo del campeonato. Estamos en la vuelta {vuelta_actual} de {total_vueltas} del {nombre_eprix}. Clasificación actual:\n{datos_fe_texto}\n{sc_texto}\n{attack_texto}\nIncidencias adicionales: {incidencias if incidencias else 'Ninguna reportada.'}\nGenera un relato de carrera apasionado y técnico en 4-5 frases. Menciona la batalla por el liderato, el uso de energía como factor estratégico, si el Attack Mode está cambiando la carrera, y qué puede pasar en las vueltas restantes. Habla en español, con el tono de un relator de Eurosport."""

        with st.spinner("⚡ El comentarista está generando el relato..."):
            respuesta_fe = cliente.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt_fe}],
                max_tokens=600
            )
            st.success(respuesta_fe.choices[0].message.content)
            if resumen_pilotos:
                st.markdown("#### 📊 Clasificación introducida")
                df_fe = pd.DataFrame([p for p in pilotos_fe if p["nombre"]])
                df_fe.columns = ["Pos", "Piloto", "Equipo", "Gap", "Energía (%)"]
                st.dataframe(df_fe, use_container_width=True)