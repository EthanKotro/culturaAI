from rest_framework import serializers
from .models import AIModel, ModelRequest, LanguageModel


class AIModelSerializer(serializers.ModelSerializer):
    """Serializer for AI Model"""
    
    class Meta:
        model = AIModel
        fields = [
            'id', 'name', 'model_type', 'version', 'is_active', 'is_default',
            'max_input_length', 'supported_languages', 'average_processing_time',
            'total_requests', 'success_rate', 'description', 'created_at'
        ]
        read_only_fields = [
            'id', 'average_processing_time', 'total_requests', 'success_rate', 'created_at'
        ]


class ModelRequestSerializer(serializers.ModelSerializer):
    """Serializer for Model Request"""
    model_name = serializers.CharField(source='model.name', read_only=True)
    
    class Meta:
        model = ModelRequest
        fields = [
            'id', 'model_name', 'input_text', 'output_text', 'source_language',
            'target_language', 'processing_time', 'success', 'error_message',
            'timestamp'
        ]


class LanguageModelSerializer(serializers.ModelSerializer):
    """Serializer for Language Model"""
    translation_model_name = serializers.CharField(source='translation_model.name', read_only=True)
    tts_model_name = serializers.CharField(source='tts_model.name', read_only=True)
    asr_model_name = serializers.CharField(source='asr_model.name', read_only=True)
    
    class Meta:
        model = LanguageModel
        fields = [
            'language_code', 'language_name', 'is_supported', 'quality_score',
            'translation_model_name', 'tts_model_name', 'asr_model_name'
        ]