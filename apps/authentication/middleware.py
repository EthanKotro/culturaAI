"""
Firebase Authentication Middleware
"""
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from firebase_admin import auth
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class FirebaseAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate users with Firebase tokens
    """
    
    def process_request(self, request):
        # Skip authentication for admin and static files
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return None
        
        # Get token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            request.user = AnonymousUser()
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            # Verify Firebase token
            decoded_token = auth.verify_id_token(token)
            firebase_uid = decoded_token['uid']
            
            # Get or create user
            try:
                user = User.objects.get(firebase_uid=firebase_uid)
                request.user = user
            except User.DoesNotExist:
                # Create new user
                user_data = {
                    'firebase_uid': firebase_uid,
                    'email': decoded_token.get('email', ''),
                    'username': decoded_token.get('email', firebase_uid),
                    'first_name': decoded_token.get('name', '').split(' ')[0] if decoded_token.get('name') else '',
                    'last_name': ' '.join(decoded_token.get('name', '').split(' ')[1:]) if decoded_token.get('name') else '',
                    'is_active': True,
                }
                
                user = User.objects.create_user(**user_data)
                request.user = user
                
                # Create user preferences
                from .models import UserPreferences
                UserPreferences.objects.create(user=user)
                
        except Exception as e:
            logger.error(f"Firebase authentication error: {str(e)}")
            request.user = AnonymousUser()
        
        return None