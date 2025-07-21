from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "facebook/nllb-200-distilled-600M"
save_dir = "./models/nllb-distilled-v1.0"

print(f"Downloading and saving model to {save_dir}...")

# Load and download to cache
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

# Save to local folder
tokenizer.save_pretrained(save_dir)
model.save_pretrained(save_dir)

print("✅ Done. Model is saved locally.")
