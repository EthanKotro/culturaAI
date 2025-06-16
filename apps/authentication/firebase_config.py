"""
Firebase configuration settings
"""
import firebase_admin
from firebase_admin import credentials
from django.conf import settings

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIALS)
    firebase_admin.initialize_app(cred)

# Firebase project configuration
FIREBASE_CONFIG = {
    'api_key': settings.FIREBASE_API_KEY,
    'auth_domain': settings.FIREBASE_AUTH_DOMAIN,
    'database_url': settings.FIREBASE_DATABASE_URL,
    'project_id': settings.FIREBASE_PROJECT_ID,
    'storage_bucket': settings.FIREBASE_STORAGE_BUCKET,
    'messaging_sender_id': settings.FIREBASE_MESSAGING_SENDER_ID,
    'app_id': settings.FIREBASE_APP_ID
}
