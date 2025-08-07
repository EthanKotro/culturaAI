from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from .models import Translation, LanguagePair, TranslationCache
from .serializers import (
    TranslationSerializer, TranslationRequestSerializer,
    TranslationFeedbackSerializer, LanguagePairSerializer,
    TranslationHistorySerializer
)
import hashlib

class TranslationListView(generics.ListAPIView):
    serializer_class = TranslationHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Translation.objects.filter(user=self.request.user)
        guest_session = self.request.session.get('guest_id')
        return Translation.objects.filter(guest_session=guest_session) if guest_session else Translation.objects.none()


class TranslationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TranslationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Translation.objects.filter(user=self.request.user)
        guest_session = self.request.session.get('guest_id')
        return Translation.objects.filter(guest_session=guest_session) if guest_session else Translation.objects.none()


import requests

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def translate_text(request):
    serializer = TranslationRequestSerializer(data=request.data)
    if serializer.is_valid():
        source_text = serializer.validated_data['source_text']
        source_lang = serializer.validated_data['source_language']
        target_lang = serializer.validated_data['target_language']

        cache_key = f"{source_lang}_{target_lang}_{hashlib.md5(source_text.encode()).hexdigest()}"
        cached_translation = TranslationCache.objects.filter(source_text_hash=cache_key).first()

        if cached_translation:
            translation = Translation.objects.create(
                source_text=source_text,
                translated_text=cached_translation.translated_text,
                source_language=source_lang,
                target_language=target_lang,
                model_used='nllb-200'
            )
            return Response(TranslationSerializer(translation).data, status=status.HTTP_200_OK)

        # Use the translator microservice
        try:
            ai_response = requests.post(
                settings.TRANSLATOR_URL,  # e.g. http://translator:8001/translate/
                json={
                    "source_text": source_text,
                    "source_language": source_lang,
                    "target_language": target_lang,
                },
                timeout=100
            )
            if ai_response.status_code != 200:
                return Response({"error": "Translation service failed."}, status=ai_response.status_code)

            translated_text = ai_response.json().get("translated_text")
            print(f"Translated text: {translated_text}")
            translation = Translation.objects.create(
                source_text=source_text,
                translated_text=translated_text,
                source_language=source_lang,
                target_language=target_lang,
                model_used='nllb-200'
            )
            TranslationCache.objects.create(
                source_text_hash=cache_key,
                translated_text=translated_text,
                source_language=source_lang,
                target_language=target_lang
            )

            return Response(TranslationSerializer(translation).data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def rate_translation(request, translation_id):
    try:
        if request.user.is_authenticated:
            translation = Translation.objects.get(id=translation_id, user=request.user)
        else:
            guest_session = request.session.get('guest_id')
            translation = Translation.objects.get(id=translation_id, guest_session=guest_session)

        rating = request.data.get('rating')
        if rating and 1 <= int(rating) <= 5:
            translation.user_rating = int(rating)
            translation.save()
            language_pair = LanguagePair.objects.get(
                source_language=translation.source_language,
                target_language=translation.target_language
            )
            language_pair.update_statistics()
            return Response({'message': 'Rating saved successfully'})
        else:
            return Response({'error': 'Rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)

    except Translation.DoesNotExist:
        return Response({'error': 'Translation not found'}, status=status.HTTP_404_NOT_FOUND)


class TranslationFeedbackView(generics.CreateAPIView):
    serializer_class = TranslationFeedbackSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class LanguagePairStatsView(generics.ListAPIView):
    serializer_class = LanguagePairSerializer
    permission_classes = [permissions.AllowAny]
    queryset = LanguagePair.objects.filter(is_active=True)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def supported_languages(request):
    return Response(settings.SUPPORTED_LANGUAGES)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def toggle_favorite(request, translation_id):
    try:
        if request.user.is_authenticated:
            translation = Translation.objects.get(id=translation_id, user=request.user)
        else:
            guest_session = request.session.get('guest_id')
            translation = Translation.objects.get(id=translation_id, guest_session=guest_session)

        translation.is_favorite = not translation.is_favorite
        translation.save()

        return Response({
            'is_favorite': translation.is_favorite,
            'message': 'Favorite status updated'
        })

    except Translation.DoesNotExist:
        return Response({'error': 'Translation not found'}, status=status.HTTP_404_NOT_FOUND)
