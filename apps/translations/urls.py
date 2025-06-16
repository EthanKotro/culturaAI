from django.urls import path
from . import views

urlpatterns = [
    path('', views.TranslationListView.as_view(), name='translation-list'),
    path('<int:pk>/', views.TranslationDetailView.as_view(), name='translation-detail'),
    path('translate/', views.translate_text, name='translate-text'),
    path('<int:translation_id>/rate/', views.rate_translation, name='rate-translation'),
    path('<int:translation_id>/favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('feedback/', views.TranslationFeedbackView.as_view(), name='translation-feedback'),
    path('language-pairs/', views.LanguagePairStatsView.as_view(), name='language-pairs'),
    path('supported-languages/', views.supported_languages, name='supported-languages'),
]