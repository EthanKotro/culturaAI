"""
Django settings for Cultura AI project.
"""

import os
from pathlib import Path
from decouple import config
import firebase_admin
from firebase_admin import credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-cultura-ai-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'django_celery_beat',
    'django_celery_results',
]

LOCAL_APPS = [
    'apps.authentication',
    'apps.translations',
    'apps.stories',
    'apps.games',
    'apps.analytics',
    'apps.ai_models',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cultura_ai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cultura_ai.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': config('DB_NAME', default='cultura_ai'),
        # 'USER': config('DB_USER', default='postgres'),
        # 'PASSWORD': config('DB_PASSWORD', default=''),
        # 'HOST': config('DB_HOST', default='localhost'),
        # 'PORT': config('DB_PORT', default='5432'),
    }
}

AUTH_USER_MODEL = 'authentication.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.authentication.authentication.FirebaseAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True

# Firebase configuration
FIREBASE_ADMIN_CREDENTIALS = os.path.join(BASE_DIR, 'firebase-adminsdk.json')

# Firebase configuration
FIREBASE_CONFIG = {
    'type': 'service_account',
    'project_id': 'culturatranslator-a',
    'auth_domain': 'culturatranslator-a.firebaseapp.com',
    'database_url': 'https://culturatranslator-a.firebaseio.com',
    'storage_bucket': 'culturatranslator-a.appspot.com',
    'messaging_sender_id': '825829097763',
    'app_id': '1:825829097763:web:d7f29544c8c9d506b54c96',
    'measurement_id': 'G-07GD4G4ER0'
}

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(FIREBASE_ADMIN_CREDENTIALS)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Firebase initialization error: {e}")

# Celery Configuration
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# AI Models Configuration
AI_MODELS = {
    'TRANSLATION': {
        'MODEL_NAME': 'facebook/nllb-200-distilled-600M',
        'CACHE_DIR': BASE_DIR / 'ai_cache' / 'translation',
        'MAX_LENGTH': 512,
    },
    'TTS': {
        'MODEL_NAME': 'tts_models/multilingual/multi-dataset/xtts_v2',
        'CACHE_DIR': BASE_DIR / 'ai_cache' / 'tts',
        'SAMPLE_RATE': 22050,
    },
    'ASR': {
        'MODEL_NAME': 'openai/whisper-base',
        'CACHE_DIR': BASE_DIR / 'ai_cache' / 'asr',
    }
}

# Language Configuration
SUPPORTED_LANGUAGES = {
    'en': {'name': 'English', 'native_name': 'English', 'flag': '🇺🇸', 'nllb_code': 'eng_Latn'},
    'ki': {'name': 'Kikuyu', 'native_name': 'Gĩkũyũ', 'flag': '🇰🇪', 'nllb_code': 'kik_Latn'},
    'luo': {'name': 'Luo', 'native_name': 'Dholuo', 'flag': '🇰🇪', 'nllb_code': 'luo_Latn'},
    'kam': {'name': 'Kamba', 'native_name': 'Kikamba', 'flag': '🇰🇪', 'nllb_code': 'kam_Latn'},
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'cultura_ai.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'cultura_ai': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Create necessary directories
os.makedirs(BASE_DIR / 'logs', exist_ok=True)
os.makedirs(BASE_DIR / 'ai_cache', exist_ok=True)
os.makedirs(BASE_DIR / 'ai_cache' / 'translation', exist_ok=True)
os.makedirs(BASE_DIR / 'ai_cache' / 'tts', exist_ok=True)
os.makedirs(BASE_DIR / 'ai_cache' / 'asr', exist_ok=True)