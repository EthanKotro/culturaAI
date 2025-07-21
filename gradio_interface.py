import gradio as gr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline


def translate(text,src_lang="eng_Latn",tgt_lang="swh_Latn"):
    model_path='./models/nllb-distilled-v1.0'
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    translator = pipeline("translation", model=model, tokenizer=tokenizer)  
    translated_text = translator(text, src_lang=src_lang, tgt_lang=tgt_lang)
    return translated_text[0]['translation_text']

gr.Interface(
    fn=translate,
    inputs=[
        gr.Textbox(label="Input Text")
    ],
    outputs=[
        gr.Textbox(label="Translated Text")
    ],
    title="English ↔ Swahili Translator"
).launch()
