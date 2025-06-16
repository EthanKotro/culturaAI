from django.contrib import admin
from .models import AIModel, ModelRequest, ModelCache, LanguageModel


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    """AI Model Admin"""
    list_display = [
        'name', 'model_type', 'version', 'is_active', 'is_default',
        'total_requests', 'success_rate', 'average_processing_time'
    ]
    list_filter = ['model_type', 'is_active', 'is_default', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = [
        'total_requests', 'success_rate', 'average_processing_time', 'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'model_type', 'model_path', 'version', 'description')
        }),
        ('Configuration', {
            'fields': ('is_active', 'is_default', 'max_input_length', 'supported_languages')
        }),
        ('Performance Metrics', {
            'fields': ('total_requests', 'success_rate', 'average_processing_time'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_models', 'deactivate_models', 'reset_metrics']
    
    def activate_models(self, request, queryset):
        queryset.update(is_active=True)
    activate_models.short_description = "Activate selected models"
    
    def deactivate_models(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_models.short_description = "Deactivate selected models"
    
    def reset_metrics(self, request, queryset):
        queryset.update(total_requests=0, success_rate=0.0, average_processing_time=0.0)
    reset_metrics.short_description = "Reset performance metrics"


@admin.register(ModelRequest)
class ModelRequestAdmin(admin.ModelAdmin):
    """Model Request Admin"""
    list_display = [
        'id', 'model', 'source_language', 'target_language',
        'processing_time', 'success', 'timestamp'
    ]
    list_filter = ['model', 'success', 'source_language', 'target_language', 'timestamp']
    search_fields = ['input_text', 'output_text', 'error_message']
    readonly_fields = ['timestamp']
    raw_id_fields = ['model']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False  # Requests are created programmatically


@admin.register(ModelCache)
class ModelCacheAdmin(admin.ModelAdmin):
    """Model Cache Admin"""
    list_display = [
        'model', 'input_preview', 'hit_count', 'created_at', 'last_accessed', 'expires_at'
    ]
    list_filter = ['model', 'created_at', 'expires_at']
    search_fields = ['input_text', 'output_text']
    readonly_fields = ['input_hash', 'created_at', 'last_accessed']
    raw_id_fields = ['model']
    
    def input_preview(self, obj):
        return obj.input_text[:50] + '...' if len(obj.input_text) > 50 else obj.input_text
    input_preview.short_description = 'Input Text'
    
    actions = ['clear_expired_cache', 'clear_low_hit_cache']
    
    def clear_expired_cache(self, request, queryset):
        from django.utils import timezone
        expired = queryset.filter(expires_at__lt=timezone.now())
        count = expired.count()
        expired.delete()
        self.message_user(request, f"Cleared {count} expired cache entries")
    clear_expired_cache.short_description = "Clear expired cache entries"
    
    def clear_low_hit_cache(self, request, queryset):
        low_hit = queryset.filter(hit_count__lt=3)
        count = low_hit.count()
        low_hit.delete()
        self.message_user(request, f"Cleared {count} low-hit cache entries")
    clear_low_hit_cache.short_description = "Clear low-hit cache entries"


@admin.register(LanguageModel)
class LanguageModelAdmin(admin.ModelAdmin):
    """Language Model Admin"""
    list_display = [
        'language_name', 'language_code', 'is_supported', 'quality_score',
        'translation_model', 'tts_model', 'asr_model'
    ]
    list_filter = ['is_supported', 'language_code']
    search_fields = ['language_name', 'language_code']
    raw_id_fields = ['translation_model', 'tts_model', 'asr_model']
    
    fieldsets = (
        ('Language Information', {
            'fields': ('language_code', 'language_name', 'is_supported', 'quality_score')
        }),
        ('Model Assignments', {
            'fields': ('translation_model', 'tts_model', 'asr_model')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']