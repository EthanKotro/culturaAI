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
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load NLLB model and tokenizer locally
HF_MODEL = "facebook/nllb-200-distilled-600M"
model = AutoModelForSeq2SeqLM.from_pretrained(HF_MODEL)
tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
translator = pipeline("translation", model=model, tokenizer=tokenizer)

# Map ISO-639-1 codes to NLLB language codes
LANGUAGE_MAP = {
    'en': 'eng_Latn',  # English
    'es': 'spa_Latn',  # Spanish
    'fr': 'fra_Latn',  # French
    'de': 'deu_Latn',  # German
    'it': 'ita_Latn',  # Italian
    'pt': 'por_Latn',  # Portuguese
    'nl': 'nld_Latn',  # Dutch
    'sv': 'swe_Latn',  # Swedish
    'da': 'dan_Latn',  # Danish
    'no': 'nob_Latn',  # Norwegian Bokmål
    'sw': 'swh_Latn',  # Swahili
    # Add more as needed
}



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


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def translate_text(request):
    """Translate text between supported languages using NLLB model"""
    serializer = TranslationRequestSerializer(data=request.data)
    if serializer.is_valid():
        source_text = serializer.validated_data['source_text']
        source_lang = serializer.validated_data['source_language']
        target_lang = serializer.validated_data['target_language']

        # Check if translation exists in cache
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

        # Get language codes for NLLB
        source_code = LANGUAGE_MAP.get(source_lang)
        target_code = LANGUAGE_MAP.get(target_lang)

        if not source_code or not target_code:
            return Response({"error": "Unsupported language pair"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Translate using NLLB pipeline
            translated_text = translator(
                source_text,
                src_lang=source_code,
                tgt_lang=target_code
            )[0]['translation_text']

            # Create translation and cache entry
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
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
