import requests
from groq import Groq
import os

cliente = Groq(api_key="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")

# URL del audio de Verstappen
url_audio = "https://livetiming.formula1.com/static/2025/2025-06-15_Canadian_Grand_Prix/2025-06-14_Practice_3/TeamRadio/MAXVER01_1_20250614_130506.mp3"

# Descargamos el audio temporalmente
print("Descargando audio...")
respuesta = requests.get(url_audio)
with open("radio_temp.mp3", "wb") as f:
    f.write(respuesta.content)

# Transcribimos con Whisper de Groq
print("Transcribiendo...")
with open("radio_temp.mp3", "rb") as f:
    transcripcion = cliente.audio.transcriptions.create(
        file=("radio_temp.mp3", f.read()),
        model="whisper-large-v3",
        language="en"
    )

print("\nTranscripción:")
print(transcripcion.text)

# Limpiamos el archivo temporal
os.remove("radio_temp.mp3")