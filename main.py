# xtts_api.py
from fastapi import FastAPI, Request, Response
import torch
from TTS.api import TTS
import io
import numpy as np
from scipy.io.wavfile import write as write_wav
import torch
from TTS.config import BaseDatasetConfig
from TTS.tts.models.xtts import XttsArgs
from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig

VOICE_MAP = {
    "english_female": "models/models--coqui--XTTS-v2/snapshots/6c2b0d75eae4b7047358e3b6bd9325f857d43f77/samples/en_sample.wav",
    "spanish_male": "models/models--coqui--XTTS-v2/snapshots/6c2b0d75eae4b7047358e3b6bd9325f857d43f77/samples/es_sample.wav"
}
DEFAULT_VOICE = "english_female"

model_path = "models/models--coqui--XTTS-v2/snapshots/6c2b0d75eae4b7047358e3b6bd9325f857d43f77"
config_path = "models/models--coqui--XTTS-v2/snapshots/6c2b0d75eae4b7047358e3b6bd9325f857d43f77/config.json"

with torch.serialization.safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs]):
    tts = TTS()
    tts.load_tts_model_by_path(
        model_path=model_path,
        config_path=config_path,
        gpu=torch.cuda.is_available()
    )
print("using device: ", torch.cuda.get_device_name(0))
app = FastAPI()
@app.post("/tts")
async def generate_tts(request: Request):
    data = await request.json()
    text = data.get("text", "")
    language = data.get("language", "en")
    voice = data.get("voice", DEFAULT_VOICE)

    if not text:
        return {"error": "Text is required"}

    speaker_wav = VOICE_MAP.get(voice, VOICE_MAP[DEFAULT_VOICE])
    
    # Generate audio as a NumPy float32 array
    wav_data = tts.tts(
        text=text,
        speaker_wav=speaker_wav,
        language=language,
    )

    # XTTS returns float32 [-1, 1]; we need to convert to int16
    int16_wav = (np.array(wav_data) * 32767).astype(np.int16)

    # Write it to a BytesIO buffer as a valid WAV file
    buffer = io.BytesIO()
    write_wav(buffer, rate=24000, data=int16_wav)
    buffer.seek(0)

    # Return with proper headers
    return Response(
        content=buffer.read(),
        media_type="audio/wav",
        headers={
            "Content-Disposition": 'inline; filename="output.wav"',
            "Content-Type": "audio/wav"
        }
    )