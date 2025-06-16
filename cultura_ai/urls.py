"""
URL configuration for Cultura AI project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# API Router
router = DefaultRouter()

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/', include([
        path('auth/', include('apps.authentication.urls')),
        path('translations/', include('apps.translations.urls')),
        path('stories/', include('apps.stories.urls')),
        path('games/', include('apps.games.urls')),
        path('analytics/', include('apps.analytics.urls')),
        path('ai/', include('apps.ai_models.urls')),
    ])),
    
    # API Root
    path('api/v1/', include(router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Cultura AI Administration"
admin.site.site_title = "Cultura AI Admin"
admin.site.index_title = "Welcome to Cultura AI Administration"