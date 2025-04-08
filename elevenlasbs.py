import os
from dotenv import load_dotenv
import requests

# Cargar variables desde .env
load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise ValueError("No se encontró la clave de API de ElevenLabs en las variables de entorno.")

VOICE_ID = 'FGY2WhTYpPnrIDTdsKH5'  # Voz por defecto de ElevenLabs
TEXTO = 'Hola, esto es una prueba con ElevenLabs y Python.'
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "audio/mpeg"
}

data = {
    "text": TEXTO,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
}

# Función para obtener el siguiente ID incremental
def get_next_id():
    counter_file = "counter.txt"

    # Si el archivo no existe, iniciar el contador en 1
    if not os.path.exists(counter_file):
        with open(counter_file, "w") as f:
            f.write("1")  # Comenzar desde el ID 1

    # Leer el último ID y actualizarlo
    with open(counter_file, "r") as f:
        last_id = int(f.read().strip())

    # Incrementar el ID
    next_id = last_id + 1

    # Guardar el nuevo ID en el archivo
    with open(counter_file, "w") as f:
        f.write(str(next_id))

    return next_id

# Enviar solicitud POST a la API de ElevenLabs
response = requests.post(url, headers=headers, json=data)

# Comprobar la respuesta
if response.status_code == 200:
    # Obtener el siguiente ID incremental
    next_id = get_next_id()

    # Usar el ID para nombrar el archivo de audio
    filename = f"audio_{next_id}.mp3"

    # Guardar el archivo de audio con un nombre único basado en el ID incremental
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"✅ Audio guardado como {filename}")
else:
    print(f"❌ Error {response.status_code}: {response.text}")
