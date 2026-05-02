import streamlit as st
import os
import requests
import base64
import time
import pandas as pd
from groq import Groq
from pilotos_fe import PILOTOS_FE, CHAMPIONSHIP_ID, EVENT_ID_BERLIN

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
    </style>
    <div class="welcome-container">
        <img class="welcome-logo" src="data:image/png;base64,{logo_b64}" alt="Paddock y Pluma">
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

try:
    font_response = requests.get("https://www.fiaformulae.com/resources/v4.37.8/fonts/FESans.var.woff2", timeout=5)
    font_b64 = base64.b64encode(font_response.content).decode()
    font_face = f"url(data:font/woff2;base64,{font_b64})"
except:
    font_face = "sans-serif"

if categoria == "Fórmula 1":
    grad_start, grad_end, accent, accent2 = "#ff1e00", "#15151e", "#ff1e00", "#ff6b35"
else:
    grad_start, grad_end, accent, accent2 = "#071c98", "#0000f4", "#0000f4", "#4d6eff"

st.markdown(f"""
<style>
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
</style>
""", unsafe_allow_html=True)

# ── FUNCIONES OPENF1 ──────────────────────────────────────────────────────────

def obtener_todas_las_carreras():
    url = "https://api.openf1.org/v1/sessions?session_type=Race&year=2026"
    r = requests.get(url)
    if r.status_code == 200:
        return [s for s in r.json() if s.get("session_name") == "Race"]
    return []

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

# ── BLOQUE FÓRMULA 1 ──────────────────────────────────────────────────────────

if categoria == "Fórmula 1":
    sesion = obtener_sesion_actual()

    if sesion:
        nombre_carrera = sesion.get("location") or "Gran Premio"
        nombre_sesion = sesion.get("session_name") or "Race"
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
            orden_pilotos.append(piloto_info.get("full_name", f"Piloto #{numero}"))

        # ── CLASIFICACIÓN ─────────────────────────────────────────────────────
        st.subheader("Clasificación final")
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
            tiempo_str = f"{int(mejor_vuelta // 60)}:{mejor_vuelta % 60:06.3f}" if mejor_vuelta else "—"
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            col1.write(posicion)
            col2.write(nombre)
            col3.write(equipo)
            col4.write(tiempo_str)

        st.markdown("---")

        # ── EVOLUCIÓN DEL RITMO ───────────────────────────────────────────────
        st.subheader("Evolución del ritmo de carrera")
        registros = []
        for vuelta in vueltas_raw:
            numero = vuelta.get("driver_number")
            lap_num = vuelta.get("lap_number")
            lap_dur = vuelta.get("lap_duration")
            if numero and lap_num and lap_dur and lap_dur < 200:
                piloto_info = pilotos_dict.get(numero, {})
                registros.append({"Vuelta": lap_num, "Piloto": piloto_info.get("full_name", f"Piloto #{numero}"), "Tiempo (s)": round(lap_dur, 3)})

        if registros:
            df_ritmo = pd.DataFrame(registros)
            todos_pilotos = sorted(df_ritmo["Piloto"].unique())
            pilotos_grafica = st.multiselect("🏎️ Selecciona pilotos para comparar", options=todos_pilotos, default=todos_pilotos[:3])
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
        st.subheader("Estrategia de neumáticos")
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
                compuesto = (stint.get("compound") or "UNKNOWN").upper()
                lap_start = stint.get("lap_start", "—")
                lap_end = stint.get("lap_end", "—")
                duracion = lap_end - lap_start + 1 if isinstance(lap_start, int) and isinstance(lap_end, int) else "—"
                filas.append({
                    "Piloto": piloto_info.get("full_name", f"Piloto #{numero}"),
                    "Stint": stint.get("stint_number", "—"),
                    "Compuesto": COLORES_COMPUESTO.get(compuesto, compuesto),
                    "Vuelta inicio": lap_start, "Vuelta fin": lap_end, "Vueltas": duracion
                })
            if filas:
                df_stints = pd.DataFrame(filas)
                df_stints["_orden"] = df_stints["Piloto"].apply(lambda x: orden_pilotos.index(x) if x in orden_pilotos else 99)
                df_stints = df_stints.sort_values(["_orden", "Stint"]).drop(columns=["_orden"])
                st.dataframe(df_stints, use_container_width=True, hide_index=True)
            else:
                st.warning("No hay datos de stints disponibles.")
        else:
            st.warning("No hay datos de estrategia disponibles para esta sesión.")

        st.markdown("---")

        # ── SECTORES ─────────────────────────────────────────────────────────
        st.subheader("Mejores tiempos por sector")
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
            df_best = df_sec.groupby("Piloto").agg(S1=("S1", "min"), S2=("S2", "min"), S3=("S3", "min")).reset_index()
            mejor_s1, mejor_s2, mejor_s3 = df_best["S1"].min(), df_best["S2"].min(), df_best["S3"].min()

            def fmt_sector(val, mejor):
                if pd.isna(val):
                    return "—"
                texto = f"{val:.3f}s"
                return f"🟣 {texto}" if val == mejor else texto

            df_best["Sector 1"] = df_best["S1"].apply(lambda x: fmt_sector(x, mejor_s1))
            df_best["Sector 2"] = df_best["S2"].apply(lambda x: fmt_sector(x, mejor_s2))
            df_best["Sector 3"] = df_best["S3"].apply(lambda x: fmt_sector(x, mejor_s3))
            df_best["_orden"] = df_best["Piloto"].apply(lambda x: orden_pilotos.index(x) if x in orden_pilotos else 99)
            df_best = df_best.sort_values("_orden")
            st.dataframe(df_best[["Piloto", "Sector 1", "Sector 2", "Sector 3"]], use_container_width=True, hide_index=True)
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
                st.caption("Refrescando cada 30 segundos automáticamente.")
        if modo_directo:
            time.sleep(30)
            st.rerun()

        st.markdown("---")

        # ── TELEMETRÍA POR PILOTO ─────────────────────────────────────────────
        st.subheader("Telemetría por piloto")
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
        st.subheader("Radios de equipo")
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
                                        with st.spinner("Transcribiendo audio..."):
                                            try:
                                                audio_response = requests.get(url_audio)
                                                nombre_temp = f"radio_temp_{i}.mp3"
                                                with open(nombre_temp, "wb") as f:
                                                    f.write(audio_response.content)
                                                with open(nombre_temp, "rb") as f:
                                                    transcripcion = cliente.audio.transcriptions.create(
                                                        file=(nombre_temp, f.read()),
                                                        model="whisper-large-v3",
                                                        language="en"
                                                    )
                                                os.remove(nombre_temp)
                                                texto_original = transcripcion.text
                                                prompt_resumen = f"""Eres un experto en Fórmula 1.
Esta es una radio de equipo de {piloto_radio} durante el {nombre_oficial}:
"{texto_original}"
Tradúcela al español y dame en 1-2 frases qué está comunicando el piloto o el equipo
y qué importancia estratégica tiene en la carrera."""
                                                respuesta_resumen = cliente.chat.completions.create(
                                                    model="llama-3.3-70b-versatile",
                                                    messages=[{"role": "user", "content": prompt_resumen}],
                                                    max_tokens=200
                                                )
                                                st.markdown(f"**Transcripción:** {texto_original}")
                                                st.success(respuesta_resumen.choices[0].message.content)
                                            except Exception as e:
                                                st.error(f"Error al transcribir: {e}")
                                else:
                                    st.warning("Audio no disponible")
                    else:
                        st.warning("No hay radios disponibles para este piloto en esta sesión.")
                else:
                    st.warning("No se pudieron cargar las radios.")

        st.markdown("---")

        # ── COMPARATIVA ENTRE DOS PILOTOS ─────────────────────────────────────
        st.subheader("Comparativa entre pilotos")
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
        st.subheader("Ingeniero de Carrera IA")
        if st.button("⚡ Analizar carrera"):
            resumen_datos = []
            for entrada in clasificacion[:20]:
                numero = entrada.get("driver_number")
                piloto_info = pilotos_dict.get(numero, {})
                nombre = piloto_info.get("full_name", f"Piloto #{numero}")
                equipo = piloto_info.get("team_name", "—")
                posicion = entrada.get("position", "—")
                mejor_vuelta = mejores_vueltas.get(numero)
                tiempo_str = f"{int(mejor_vuelta // 60)}:{mejor_vuelta % 60:06.3f}" if mejor_vuelta else "—"
                resumen_datos.append(f"P{posicion}: {nombre} ({equipo}) — Mejor vuelta: {tiempo_str}")

            prompt = f"""Eres un ingeniero de carrera experto de Fórmula 1. Acabas de ver los resultados finales del {nombre_oficial}. Clasificación:\n{chr(10).join(resumen_datos)}\nAnaliza en 4-5 frases con pasión y criterio técnico. Habla en español."""
            with st.spinner("El ingeniero está analizando la carrera..."):
                respuesta = cliente.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024
                )
                st.success(respuesta.choices[0].message.content)

    else:
        st.warning("No se pudo cargar la sesión. Comprueba tu conexión.")

elif categoria == "Formula E":

    def obtener_standings_fe():
        url = "https://stats-centre.fiaformulae.com/prod/api/realtime/standings"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.json().get("data", {}).get("standings", {})
        except:
            pass
        return {}

    def obtener_mejores_vueltas_fe():
        url = f"https://stats-centre.fiaformulae.com/prod/api/details/best-lap-timings?championshipId={CHAMPIONSHIP_ID}&eventId={EVENT_ID_BERLIN}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json().get("data", [])
                if data:
                    return data[0].get("participants", {})
        except:
            pass
        return {}

    def obtener_sectores_fe():
        url = f"https://stats-centre.fiaformulae.com/prod/api/details/sectortiming?championshipId={CHAMPIONSHIP_ID}&eventId={EVENT_ID_BERLIN}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json().get("data", [])
                if data:
                    return data[0].get("participants", {})
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

    st.subheader("Berlin E-Prix 2026 — En directo")

    col_live1, col_live2 = st.columns([1, 3])
    with col_live1:
        modo_directo_fe = st.toggle("Modo en directo", key="live_fe")
    with col_live2:
        if modo_directo_fe:
            st.caption("Refrescando cada 30 segundos automáticamente.")

    standings = obtener_standings_fe()
    mejores_vueltas_fe = obtener_mejores_vueltas_fe()
    sectores_fe = obtener_sectores_fe()

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

            col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 2, 2, 2])
            col1.write(posicion)
            col2.write(piloto_info["nombre"])
            col3.write(piloto_info["equipo"])
            col4.write(gap_str)
            col5.write(tiempo_str)
            col6.write(cambio_str)

        st.markdown("---")

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
                df_sec_fe = pd.DataFrame(filas_sec)
                st.dataframe(df_sec_fe, use_container_width=True, hide_index=True)

        st.markdown("---")

        st.subheader("Ingeniero de Carrera IA")

        if st.button("Analizar sesión FE"):
            resumen_fe = []
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

            datos_fe_texto = "\n".join(resumen_fe)

            prompt_fe = f"""Eres un comentarista experto de Formula E con conocimiento técnico profundo del campeonato.
Estos son los datos en tiempo real del Berlin E-Prix 2026:

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

    else:
        st.info("No hay datos en tiempo real disponibles. La sesión puede no estar activa.")
        st.markdown("**Próximas sesiones del Berlin E-Prix:**")
        st.markdown("- Qualifying Group A y B — Hoy")
        st.markdown("- Carrera — Mañana")

    if modo_directo_fe:
        time.sleep(30)
        st.rerun()