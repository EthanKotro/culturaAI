"""
Firebase Authentication Backend for Django REST Framework
"""
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
from firebase_admin import auth
from .firebase_init import get_firebase_app

User = get_user_model()


class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    Firebase token authentication.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:
        Authorization: Bearer your-firebase-id-token
    """
   
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        
        if not auth_header or auth_header[0].lower() != b'bearer':
            return None

        if len(auth_header) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth_header[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            # Initialize Firebase if needed
            get_firebase_app()
            
            # Verify Firebase ID token
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            
            # Get or create Django user
            user, created = User.objects.get_or_create(username=uid)
            
            # Update user info from Firebase if needed
            if created or not hasattr(user, 'firebase_uid'):
                firebase_user = auth.get_user(uid)
                user.firebase_uid = uid
                user.email = firebase_user.email
                user.save()

            return (user, token)
        except auth.InvalidIdTokenError:
            raise exceptions.AuthenticationFailed('Invalid Firebase ID token')
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))
            return None
        
        if len(auth_header) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        
        return self.authenticate_credentials(token)
    
    def authenticate_credentials(self, token):
        try:
            # Verify the Firebase token
            decoded_token = auth.verify_id_token(token)
            firebase_uid = decoded_token['uid']
            
            # Get or create user
            try:
                user = User.objects.get(firebase_uid=firebase_uid)
            except User.DoesNotExist:
                # Create new user from Firebase token
                user_data = {
                    'firebase_uid': firebase_uid,
                    'email': decoded_token.get('email', ''),
                    'username': decoded_token.get('email', firebase_uid),
                    'first_name': decoded_token.get('name', '').split(' ')[0] if decoded_token.get('name') else '',
                    'last_name': ' '.join(decoded_token.get('name', '').split(' ')[1:]) if decoded_token.get('name') else '',
                    'is_active': True,
                }
                
                user = User.objects.create_user(**user_data)
                
                # Create user preferences
                from .models import UserPreferences
                UserPreferences.objects.create(user=user)
            
            if not user.is_active:
                raise exceptions.AuthenticationFailed('User account is disabled.')
            
            return (user, token)
            
        except auth.InvalidIdTokenError:
            raise exceptions.AuthenticationFailed('Invalid Firebase token.')
        except auth.ExpiredIdTokenError:
            raise exceptions.AuthenticationFailed('Firebase token has expired.')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Authentication failed: {str(e)}')
    
    def authenticate_header(self, request):
        return 'Bearer'