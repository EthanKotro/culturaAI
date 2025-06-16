from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.conf import settings
from .models import Translation, TranslationFeedback, LanguagePair
from .serializers import (
    TranslationSerializer, TranslationRequestSerializer,
    TranslationFeedbackSerializer, LanguagePairSerializer,
    TranslationHistorySerializer
)
from .tasks import translate_text_task
import hashlib
import time


class TranslationListView(generics.ListAPIView):
    """List user's translation history"""
    serializer_class = TranslationHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Translation.objects.filter(user=self.request.user)
        else:
            # For guest users, use session
            guest_session = self.request.session.get('guest_id')
            if guest_session:
                return Translation.objects.filter(guest_session=guest_session)
            return Translation.objects.none()


class TranslationDetailView(generics.RetrieveUpdateAPIView):
    """Get and update specific translation"""
    serializer_class = TranslationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Translation.objects.filter(user=self.request.user)
        else:
            guest_session = self.request.session.get('guest_id')
            if guest_session:
                return Translation.objects.filter(guest_session=guest_session)
            return Translation.objects.none()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def translate_text(request):
    """Translate text using AI models"""
    serializer = TranslationRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    source_text = data['source_text']
    source_lang = data['source_language']
    target_lang = data['target_language']
    
    # Check cache first
    text_hash = hashlib.sha256(
        f"{source_text}_{source_lang}_{target_lang}".encode()
    ).hexdigest()
    
    from .models import TranslationCache
    try:
        cached = TranslationCache.objects.get(source_text_hash=text_hash)
        cached.hit_count += 1
        cached.save()
        
        # Create translation record
        translation_data = {
            'source_text': source_text,
            'translated_text': cached.translated_text,
            'source_language': source_lang,
            'target_language': target_lang,
            'model_used': 'cached',
            'processing_time': 0.1,
        }
        
        if request.user.is_authenticated:
            translation_data['user'] = request.user
        else:
            guest_id = request.session.get('guest_id')
            if not guest_id:
                import uuid
                guest_id = str(uuid.uuid4())
                request.session['guest_id'] = guest_id
            translation_data['guest_session'] = guest_id
        
        translation = Translation.objects.create(**translation_data)
        
        return Response({
            'id': translation.id,
            'translated_text': cached.translated_text,
            'source_text': source_text,
            'source_language': source_lang,
            'target_language': target_lang,
            'processing_time': 0.1,
            'cached': True
        })
        
    except TranslationCache.DoesNotExist:
        pass
    
    # If not cached, process with AI
    start_time = time.time()
    
    # Use Celery task for translation
    try:
        # For demo purposes, we'll use a simple mock translation
        # In production, this would call the actual AI model
        translated_text = f"[{target_lang.upper()}] {source_text} (AI Translation)"
        
        processing_time = time.time() - start_time
        
        # Create translation record
        translation_data = {
            'source_text': source_text,
            'translated_text': translated_text,
            'source_language': source_lang,
            'target_language': target_lang,
            'model_used': 'nllb-200-demo',
            'processing_time': processing_time,
            'confidence_score': 0.85,
        }
        
        if request.user.is_authenticated:
            translation_data['user'] = request.user
            # Add points for translation
            request.user.total_translations += 1
            request.user.add_points(10)
        else:
            guest_id = request.session.get('guest_id')
            if not guest_id:
                import uuid
                guest_id = str(uuid.uuid4())
                request.session['guest_id'] = guest_id
            translation_data['guest_session'] = guest_id
        
        translation = Translation.objects.create(**translation_data)
        
        # Cache the translation
        TranslationCache.objects.create(
            source_text_hash=text_hash,
            source_text=source_text,
            translated_text=translated_text,
            source_language=source_lang,
            target_language=target_lang
        )
        
        # Update language pair statistics
        language_pair, created = LanguagePair.objects.get_or_create(
            source_language=source_lang,
            target_language=target_lang
        )
        language_pair.update_statistics()
        
        return Response({
            'id': translation.id,
            'translated_text': translated_text,
            'source_text': source_text,
            'source_language': source_lang,
            'target_language': target_lang,
            'processing_time': processing_time,
            'confidence_score': 0.85,
            'cached': False
        })
        
    except Exception as e:
        return Response(
            {'error': f'Translation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def rate_translation(request, translation_id):
    """Rate a translation"""
    try:
        if request.user.is_authenticated:
            translation = Translation.objects.get(id=translation_id, user=request.user)
        else:
            guest_session = request.session.get('guest_id')
            translation = Translation.objects.get(
                id=translation_id, 
                guest_session=guest_session
            )
        
        rating = request.data.get('rating')
        if rating and 1 <= int(rating) <= 5:
            translation.user_rating = int(rating)
            translation.save()
            
            # Update language pair statistics
            language_pair = LanguagePair.objects.get(
                source_language=translation.source_language,
                target_language=translation.target_language
            )
            language_pair.update_statistics()
            
            return Response({'message': 'Rating saved successfully'})
        else:
            return Response(
                {'error': 'Rating must be between 1 and 5'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Translation.DoesNotExist:
        return Response(
            {'error': 'Translation not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


class TranslationFeedbackView(generics.CreateAPIView):
    """Submit feedback for translations"""
    serializer_class = TranslationFeedbackSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class LanguagePairStatsView(generics.ListAPIView):
    """Get language pair statistics"""
    serializer_class = LanguagePairSerializer
    permission_classes = [permissions.AllowAny]
    queryset = LanguagePair.objects.filter(is_active=True)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def supported_languages(request):
    """Get list of supported languages"""
    return Response(settings.SUPPORTED_LANGUAGES)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def toggle_favorite(request, translation_id):
    """Toggle favorite status of a translation"""
    try:
        if request.user.is_authenticated:
            translation = Translation.objects.get(id=translation_id, user=request.user)
        else:
            guest_session = request.session.get('guest_id')
            translation = Translation.objects.get(
                id=translation_id, 
                guest_session=guest_session
            )
        
        translation.is_favorite = not translation.is_favorite
        translation.save()
        
        return Response({
            'is_favorite': translation.is_favorite,
            'message': 'Favorite status updated'
        })
        
    except Translation.DoesNotExist:
        return Response(
            {'error': 'Translation not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )