from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from fastapi.concurrency import run_in_threadpool
import torch
import os
import time
import re

# --- FastAPI app setup ---
app = FastAPI()

# --- Request model ---
class TranslationRequest(BaseModel):
    source_text: str
    source_language: str
    target_language: str

# --- Language code map ---
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

# --- Model setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# model_path = os.getenv("MODEL_PATH", os.path.join(BASE_DIR, "models/nllb-distilled-v1.0"))
model_path = os.path.join(BASE_DIR, "models/nllb-distilled-v1.0/models--facebook--nllb-200-distilled-600M/snapshots/f8d333a098d19b4fd9a8b18f94170487ad3f821d")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 Loading model to device: {device}")

model = AutoModelForSeq2SeqLM.from_pretrained(model_path, local_files_only=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)

if device.type == "cuda":
    print("🧠 Using FP16 precision on GPU")
    model = model.half()
model = model.to(device)

# --- Split input text into chunks ---
def split_text(text, max_length=500):
    text = text.replace("“", "\"").replace("”", "\"").replace("‘", "'").replace("’", "'")
    sentences = re.split(r'([.!?]["\']?\s)', text)
    chunks = []
    current = ""

    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        if i + 1 < len(sentences):
            sentence += sentences[i + 1]
        if len(current) + len(sentence) <= max_length:
            current += sentence
        else:
            chunks.append(current.strip())
            current = sentence
    if current.strip():
        chunks.append(current.strip())
    return chunks

# --- Translation logic ---
def translate_text(source_text: str, src_lang: str, tgt_lang: str) -> str:
    tokenizer.src_lang = src_lang
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(tgt_lang)

    translated_chunks = []

    for chunk in split_text(source_text):
        encoded = tokenizer(
            chunk,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(device)

        # 🧠 Print where inputs and model live
        print(f"📦 Encoded input is on: {encoded.input_ids.device}")
        print(f"🧠 Model is on: {next(model.parameters()).device}")

        with torch.no_grad():
            generated_tokens = model.generate(
                **encoded,
                forced_bos_token_id=forced_bos_token_id,
                max_new_tokens=512,
                do_sample=False
            )

        translated = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        translated_chunks.append(translated.strip())

    return " ".join(translated_chunks)

# --- FastAPI route ---
@app.post("/translate/")
async def translate(request: TranslationRequest):
    src = LANGUAGE_MAP.get(request.source_language)
    tgt = LANGUAGE_MAP.get(request.target_language)

    if not src or not tgt:
        return {"error": "Unsupported language pair"}

    print(f"\n🌍 Translating from {src} to {tgt}")
    print(f"📄 Input text length: {len(request.source_text)} characters")

    start_time = time.time()
    translated_text = await run_in_threadpool(translate_text, request.source_text, src, tgt)
    end_time = time.time()

    translation_time = round(end_time - start_time, 2)

    print("✅ Translation complete!")
    print(f"🕒 Time taken: {translation_time} seconds")
    print("-" * 60)

    return {
        "translated_text": translated_text,
        "translation_time": translation_time
    }
