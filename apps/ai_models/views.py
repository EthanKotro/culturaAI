from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse, Http404
from .models import AIModel, ModelRequest, LanguageModel
from .serializers import AIModelSerializer, ModelRequestSerializer, LanguageModelSerializer
from .utils import generate_speech
import os


class AIModelListView(generics.ListAPIView):
    """List available AI models"""
    serializer_class = AIModelSerializer
    permission_classes = [permissions.AllowAny]
    queryset = AIModel.objects.filter(is_active=True)


class ModelRequestListView(generics.ListAPIView):
    """List model requests for monitoring"""
    serializer_class = ModelRequestSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        model_id = self.request.query_params.get('model_id')
        queryset = ModelRequest.objects.all()
        
        if model_id:
            queryset = queryset.filter(model_id=model_id)
        
        return queryset[:100]  # Limit to recent 100 requests


class LanguageModelListView(generics.ListAPIView):
    """List language-specific model configurations"""
    serializer_class = LanguageModelSerializer
    permission_classes = [permissions.AllowAny]
    queryset = LanguageModel.objects.filter(is_supported=True)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def generate_tts(request):
    """Generate text-to-speech audio"""
    text = request.data.get('text', '').strip()
    language = request.data.get('language', 'en')
    voice_settings = request.data.get('voice_settings', {})
    
    if not text:
        return Response(
            {'error': 'Text is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(text) > 1000:
        return Response(
            {'error': 'Text too long (max 1000 characters)'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Generate speech
        audio_path = generate_speech(text, language, voice_settings)
        
        # Return audio file URL
        audio_url = request.build_absolute_uri(audio_path)
        
        return Response({
            'audio_url': audio_url,
            'text': text,
            'language': language,
            'message': 'Audio generated successfully'
        })
        
    except Exception as e:
        return Response(
            {'error': f'TTS generation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def model_stats(request):
    """Get AI model statistics"""
    stats = {}
    
    for model in AIModel.objects.filter(is_active=True):
        stats[model.name] = {
            'type': model.model_type,
            'total_requests': model.total_requests,
            'success_rate': model.success_rate,
            'average_processing_time': model.average_processing_time,
            'supported_languages': model.supported_languages
        }
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def update_model_config(request, model_id):
    """Update AI model configuration"""
    try:
        model = AIModel.objects.get(id=model_id)
        
        # Update allowed fields
        allowed_fields = ['is_active', 'is_default', 'max_input_length', 'description']
        
        for field in allowed_fields:
            if field in request.data:
                setattr(model, field, request.data[field])
        
        model.save()
        
        serializer = AIModelSerializer(model)
        return Response(serializer.data)
        
    except AIModel.DoesNotExist:
        return Response(
            {'error': 'Model not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """Health check for AI models"""
    health_status = {}
    
    for model in AIModel.objects.filter(is_active=True):
        # Simple health check - in production this would test actual model loading
        health_status[model.name] = {
            'status': 'healthy' if model.success_rate > 80 else 'degraded',
            'success_rate': model.success_rate,
            'last_request': model.requests.first().timestamp if model.requests.exists() else None
        }
    
    overall_status = 'healthy' if all(
        status['status'] == 'healthy' for status in health_status.values()
    ) else 'degraded'
    
    return Response({
        'overall_status': overall_status,
        'models': health_status,
        'timestamp': request.META.get('HTTP_DATE')
    })