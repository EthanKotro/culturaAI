from django.urls import path
from .views import TTSAPIView

urlpatterns = [
    path('', TTSAPIView.as_view(), name='tts-service'),
]