from rest_framework import serializers
from .models import Translation, TranslationFeedback, LanguagePair


class TranslationSerializer(serializers.ModelSerializer):
    """Serializer for Translation model"""
    
    class Meta:
        model = Translation
        fields = [
            'id', 'source_text', 'translated_text', 'source_language',
            'target_language', 
            'created_at', 
        ]
        read_only_fields = [
            'id', 'translated_text',
            'created_at'
        ]


class TranslationRequestSerializer(serializers.Serializer):
    """Serializer for translation requests"""
    source_text = serializers.CharField(max_length=5000)
    source_language = serializers.CharField(max_length=10)
    target_language = serializers.CharField(max_length=10)
    
    def validate_source_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Source text cannot be empty")
        return value.strip()
    
    def validate(self, data):
        if data['source_language'] == data['target_language']:
            raise serializers.ValidationError(
                "Source and target languages must be different"
            )
        return data


class TranslationFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for Translation Feedback"""
    
    class Meta:
        model = TranslationFeedback
        fields = [
            'id', 'translation', 'feedback_type', 'feedback_text',
            'suggested_translation', 'created_at', 'is_reviewed'
        ]
        read_only_fields = ['id', 'created_at', 'is_reviewed']


class LanguagePairSerializer(serializers.ModelSerializer):
    """Serializer for Language Pair statistics"""
    
    class Meta:
        model = LanguagePair
        fields = [
            'source_language', 'target_language', 'total_translations',
            'average_rating', 'average_processing_time', 'is_active'
        ]
        read_only_fields = [
            'total_translations', 'average_rating', 'average_processing_time'
        ]


class TranslationHistorySerializer(serializers.ModelSerializer):
    """Simplified serializer for translation history"""
    
    class Meta:
        model = Translation
        fields = [
            'id', 'source_text', 'translated_text', 'source_language',
            'target_language', 'created_at', 'user_rating', 'is_favorite'
        ]