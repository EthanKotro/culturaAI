import gradio as gr
import requests
import os

# Get your Hugging Face API token
HF_API_TOKEN = os.getenv('HF_API_TOKEN')

# Your model name
MODEL_NAME = "EthanKotro/kikuyu-translation-train"

# API endpoint
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

def translate(text, source_lang, target_lang):
    try:
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        payload = {
            "inputs": text,
            "parameters": {
                "source_language": source_lang,
                "target_language": target_lang,
                "max_length": 100
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        
        if 'error' in result:
            return f"Error: {result['error']}"
        
        return result[0]['translation_text'] if result else "Translation failed"
        
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
demo = gr.Interface(
    fn=translate,
    inputs=[
        gr.Textbox(label="Input Text"),
        gr.Dropdown(choices=["en", "ki", "luo", "kam"], label="Source Language"),
        gr.Dropdown(choices=["en", "ki", "luo", "kam"], label="Target Language")
    ],
    outputs="text",
    title="Kikuyu Translation Hub",
    description="Translate between English and Kikuyu"
)

demo.launch()
