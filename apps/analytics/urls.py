from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_overview, name='analytics-dashboard'),
    path('languages/', views.language_analytics, name='language-analytics'),
    path('features/', views.feature_analytics, name='feature-analytics'),
    path('content/', views.content_analytics, name='content-analytics'),
    path('retention/', views.user_retention_analytics, name='retention-analytics'),
    path('track/', views.track_engagement, name='track-engagement'),
    path('export/', views.export_analytics, name='export-analytics'),
]