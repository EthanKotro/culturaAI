from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import os

# Define request model
class TranslationRequest(BaseModel):
    source_text: str
    source_language: str
    target_language: str

# Language map
LANGUAGE_MAP = {
    'en': 'eng_Latn',
    'es': 'spa_Latn',
    'fr': 'fra_Latn',
    'de': 'deu_Latn',
    'it': 'ita_Latn',
    'pt': 'por_Latn',
    'sw': 'swh_Latn',
    'ki': 'kik_Latn',
    'luo': 'luo_Latn',
    'kam': 'kam_Latn',
}

# Get model path from env or default
# model_path = os.getenv("MODEL_PATH", "./models/nllb-distilled-v1.0")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.getenv("MODEL_PATH", os.path.join(BASE_DIR, "models/nllb-distilled-v1.0"))

# Load model
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, local_files_only=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
translator = pipeline("translation", model=model, tokenizer=tokenizer)

# Initialize app
app = FastAPI()

@app.post("/translate/")
async def translate(request: TranslationRequest):
    src = LANGUAGE_MAP.get(request.source_language)
    tgt = LANGUAGE_MAP.get(request.target_language)

    if not src or not tgt:
        return {"error": "Unsupported language pair"}

    translated_text = translator(
        request.source_text,
        src_lang=src,
        tgt_lang=tgt
    )[0]["translation_text"]
    
    print(f"Translated text: {translated_text}")
    return {"translated_text": translated_text}
