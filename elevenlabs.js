require('dotenv').config();
const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Leer la clave de API desde .env
const API_KEY = process.env.ELEVENLABS_API_KEY;
if (!API_KEY) {
  throw new Error("No se encontró la clave de API de ElevenLabs en las variables de entorno.");
}

const VOICE_ID = 'FGY2WhTYpPnrIDTdsKH5';
const TEXTO = 'Hola, esto es una prueba con ElevenLabs y JavaScript.';
const url = `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`;

const headers = {
  'xi-api-key': API_KEY,
  'Content-Type': 'application/json',
  'Accept': 'audio/mpeg',
};

const data = {
  text: TEXTO,
  model_id: 'eleven_monolingual_v1',
  voice_settings: {
    stability: 0.5,
    similarity_boost: 0.5,
  },
};

// Generar nombre de archivo con timestamp
const timestamp = new Date().toISOString().replace(/[-:.]/g, '').slice(0, 15);
const fileName = `audio_${timestamp}.mp3`;
const filePath = path.join(__dirname, fileName);

// Enviar solicitud a ElevenLabs
axios.post(url, data, { headers, responseType: 'stream' })
  .then(response => {
    const writer = fs.createWriteStream(filePath);
    response.data.pipe(writer);
    writer.on('finish', () => {
      console.log(`✅ Audio guardado como ${fileName}`);
    });
    writer.on('error', err => {
      console.error('❌ Error al guardar el archivo:', err.message);
    });
  })
  .catch(error => {
    console.error(`❌ Error ${error.response?.status || ''}:`, error.response?.data || error.message);
  });
