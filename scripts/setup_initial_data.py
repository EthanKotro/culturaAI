#!/usr/bin/env python
"""
Script to set up initial data for Cultura AI
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cultura_ai.settings')
django.setup()

from apps.ai_models.models import AIModel, LanguageModel
from apps.translations.models import LanguagePair
from django.contrib.auth import get_user_model

User = get_user_model()


def create_ai_models():
    """Create initial AI models"""
    print("Creating AI models...")
    
    # Translation model
    translation_model, created = AIModel.objects.get_or_create(
        name='NLLB-200-Distilled',
        defaults={
            'model_type': 'translation',
            'model_path': 'facebook/nllb-200-distilled-600M',
            'version': '1.0',
            'is_active': True,
            'is_default': True,
            'max_input_length': 512,
            'supported_languages': ['en', 'ki', 'luo', 'kam'],
            'description': 'No Language Left Behind - 200 language translation model'
        }
    )
    
    if created:
        print(f"Created translation model: {translation_model.name}")
    
    # TTS model
    tts_model, created = AIModel.objects.get_or_create(
        name='XTTS-v2-Multilingual',
        defaults={
            'model_type': 'tts',
            'model_path': 'tts_models/multilingual/multi-dataset/xtts_v2',
            'version': '2.0',
            'is_active': True,
            'is_default': True,
            'max_input_length': 1000,
            'supported_languages': ['en', 'ki', 'luo', 'kam'],
            'description': 'XTTS v2 multilingual text-to-speech model'
        }
    )
    
    if created:
        print(f"Created TTS model: {tts_model.name}")
    
    # ASR model
    asr_model, created = AIModel.objects.get_or_create(
        name='Whisper-Base',
        defaults={
            'model_type': 'asr',
            'model_path': 'openai/whisper-base',
            'version': '1.0',
            'is_active': True,
            'is_default': True,
            'max_input_length': 30,  # 30 seconds
            'supported_languages': ['en', 'ki', 'luo', 'kam'],
            'description': 'OpenAI Whisper base model for speech recognition'
        }
    )
    
    if created:
        print(f"Created ASR model: {asr_model.name}")


def create_language_models():
    """Create language-specific model configurations"""
    print("Creating language model configurations...")
    
    languages = [
        ('en', 'English'),
        ('ki', 'Kikuyu'),
        ('luo', 'Luo'),
        ('kam', 'Kamba'),
    ]
    
    translation_model = AIModel.objects.get(model_type='translation', is_default=True)
    tts_model = AIModel.objects.get(model_type='tts', is_default=True)
    asr_model = AIModel.objects.get(model_type='asr', is_default=True)
    
    for code, name in languages:
        lang_model, created = LanguageModel.objects.get_or_create(
            language_code=code,
            defaults={
                'language_name': name,
                'translation_model': translation_model,
                'tts_model': tts_model,
                'asr_model': asr_model,
                'is_supported': True,
                'quality_score': 0.8 if code == 'en' else 0.6  # English has higher quality
            }
        )
        
        if created:
            print(f"Created language model configuration for: {name}")


def create_language_pairs():
    """Create language pair configurations"""
    print("Creating language pairs...")
    
    languages = ['en', 'ki', 'luo', 'kam']
    
    for source in languages:
        for target in languages:
            if source != target:
                pair, created = LanguagePair.objects.get_or_create(
                    source_language=source,
                    target_language=target,
                    defaults={
                        'is_active': True,
                        'model_name': 'nllb-200'
                    }
                )
                
                if created:
                    print(f"Created language pair: {source} → {target}")


def create_admin_user():
    """Create admin user if it doesn't exist"""
    print("Creating admin user...")
    
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@cultura-ai.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print(f"Created admin user: {admin_user.username}")
    else:
        print("Admin user already exists")


def main():
    """Run all setup functions"""
    print("Setting up initial data for Cultura AI...")
    
    create_ai_models()
    create_language_models()
    create_language_pairs()
    create_admin_user()
    
    print("\nInitial data setup completed successfully!")
    print("\nYou can now:")
    print("1. Start the Django development server: python manage.py runserver")
    print("2. Access the admin panel at: http://localhost:8000/admin/")
    print("3. Login with username: admin, password: admin123")
    print("4. Test the API endpoints at: http://localhost:8000/api/v1/")


if __name__ == '__main__':
    main()