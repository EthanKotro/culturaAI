from TTS.api import TTS
import torch
from TTS.config import BaseDatasetConfig
from TTS.tts.models.xtts import XttsArgs

from scipy.io.wavfile import write as write_wav

import numpy as np

import io
from torch.serialization import add_safe_globals
from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig

import warnings
warnings.filterwarnings(
    "ignore",
    message=".*this function's implementation will be changed to use torchaudio.load_with_torchcodec.*"
)

from fastapi import FastAPI,Request,Response
# Allow PyTorch to unpickle this class from the checkpoint
add_safe_globals([XttsConfig,XttsArgs,BaseDatasetConfig,XttsAudioConfig])

app = FastAPI()

model_path="./models/coqui_XTTS-v2"
config_path="./models/coqui_XTTS-v2/config.json"
speaker_wav_path="./models/coqui_XTTS-v2/samples/en_sample.wav"

model= TTS()
model.load_tts_model_by_path(model_path=model_path, config_path=config_path, gpu=torch.cuda.is_available())
if torch.cuda.is_available() : 
    print("using Cuda")
else:
    print("Using CPU")  

@app.post("/tts")
async def generate_tts(request: Request):
    data = await request.json()
    text = data.get("text", "")
    language = data.get("language", "en")

    if not text:
        return {"error": "Text is required"}

    speaker_wav = speaker_wav_path
    
    # Generate audio as a NumPy float32 array
    wav_data = model.tts(
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
# generate speech by cloning a voice using default settings
# model.tts_to_file(text="Habari yako. Leo ni siku nzuri ya kujifunza kuhusu mabadiliko ya tabianchi.",
#                 file_path="./outputs/output.wav",
#                 speaker_wav=speaker_wav_path,
#                 language="en")

