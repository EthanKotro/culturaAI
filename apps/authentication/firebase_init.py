"""
Firebase Admin SDK initialization
"""
import firebase_admin
from firebase_admin import credentials
from django.conf import settings
from pathlib import Path

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK with credentials"""
    if not firebase_admin._apps:
        try:
            # Get the base directory from settings
            base_dir = Path(settings.BASE_DIR)
            credentials_path = base_dir / 'firebase-adminsdk.json'
            
            # Check if the credentials file exists
            if not credentials_path.exists():
                print("Warning: Firebase credentials file not found. Skipping initialization.")
                return
                
            cred = credentials.Certificate(str(credentials_path))
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Error initializing Firebase: {str(e)}")
            raise

# Don't initialize Firebase when module is imported
# Instead, initialize when needed in authentication.py
# This prevents circular dependency issues with settings

def get_firebase_app():
    """Get or initialize Firebase app"""
    if not firebase_admin._apps:
        initialize_firebase()
    return firebase_admin.get_app()
