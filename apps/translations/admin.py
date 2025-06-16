from django.contrib import admin
from .models import Translation, TranslationFeedback, LanguagePair, TranslationCache


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    """Translation Admin"""
    list_display = [
        'id', 'user', 'source_language', 'target_language',
        'source_text_preview', 'user_rating', 'is_favorite',
        'model_used', 'processing_time', 'created_at'
    ]
    list_filter = [
        'source_language', 'target_language', 'model_used',
        'user_rating', 'is_favorite', 'created_at'
    ]
    search_fields = ['source_text', 'translated_text', 'user__username']
    readonly_fields = ['created_at', 'processing_time', 'confidence_score']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    
    def source_text_preview(self, obj):
        return obj.source_text[:50] + '...' if len(obj.source_text) > 50 else obj.source_text
    source_text_preview.short_description = 'Source Text'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(TranslationFeedback)
class TranslationFeedbackAdmin(admin.ModelAdmin):
    """Translation Feedback Admin"""
    list_display = [
        'id', 'translation', 'user', 'feedback_type',
        'is_reviewed', 'created_at'
    ]
    list_filter = ['feedback_type', 'is_reviewed', 'created_at']
    search_fields = ['feedback_text', 'user__username']
    readonly_fields = ['created_at']
    raw_id_fields = ['user', 'translation']
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_reviewed']
    
    def mark_as_reviewed(self, request, queryset):
        queryset.update(is_reviewed=True)
    mark_as_reviewed.short_description = "Mark selected feedback as reviewed"


@admin.register(LanguagePair)
class LanguagePairAdmin(admin.ModelAdmin):
    """Language Pair Admin"""
    list_display = [
        'source_language', 'target_language', 'total_translations',
        'average_rating', 'average_processing_time', 'is_active'
    ]
    list_filter = ['is_active', 'source_language', 'target_language']
    readonly_fields = [
        'total_translations', 'average_rating', 'average_processing_time',
        'created_at', 'updated_at'
    ]
    
    actions = ['update_statistics', 'activate_pairs', 'deactivate_pairs']
    
    def update_statistics(self, request, queryset):
        for pair in queryset:
            pair.update_statistics()
        self.message_user(request, f"Updated statistics for {queryset.count()} language pairs")
    update_statistics.short_description = "Update statistics for selected pairs"
    
    def activate_pairs(self, request, queryset):
        queryset.update(is_active=True)
    activate_pairs.short_description = "Activate selected language pairs"
    
    def deactivate_pairs(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_pairs.short_description = "Deactivate selected language pairs"


@admin.register(TranslationCache)
class TranslationCacheAdmin(admin.ModelAdmin):
    """Translation Cache Admin"""
    list_display = [
        'source_text_preview', 'source_language', 'target_language',
        'hit_count', 'created_at', 'last_accessed'
    ]
    list_filter = ['source_language', 'target_language', 'created_at']
    search_fields = ['source_text', 'translated_text']
    readonly_fields = ['source_text_hash', 'created_at', 'last_accessed']
    date_hierarchy = 'created_at'
    
    def source_text_preview(self, obj):
        return obj.source_text[:50] + '...' if len(obj.source_text) > 50 else obj.source_text
    source_text_preview.short_description = 'Source Text'
    
    actions = ['clear_low_hit_cache']
    
    def clear_low_hit_cache(self, request, queryset):
        low_hit_entries = queryset.filter(hit_count__lt=3)
        count = low_hit_entries.count()
        low_hit_entries.delete()
        self.message_user(request, f"Cleared {count} low-hit cache entries")
    clear_low_hit_cache.short_description = "Clear cache entries with low hit count"