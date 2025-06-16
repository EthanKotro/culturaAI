from django.urls import path
from . import views

urlpatterns = [
    path('models/', views.AIModelListView.as_view(), name='ai-models'),
    path('models/<int:model_id>/config/', views.update_model_config, name='update-model-config'),
    path('requests/', views.ModelRequestListView.as_view(), name='model-requests'),
    path('languages/', views.LanguageModelListView.as_view(), name='language-models'),
    path('tts/', views.generate_tts, name='generate-tts'),
    path('stats/', views.model_stats, name='model-stats'),
    path('health/', views.health_check, name='ai-health-check'),
]