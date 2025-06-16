from django.contrib import admin
from .models import (
    UserEngagement, LanguageUsage, FeatureUsage,
    ContentPerformance, SystemMetrics, UserRetention
)


@admin.register(UserEngagement)
class UserEngagementAdmin(admin.ModelAdmin):
    """User Engagement Admin"""
    list_display = [
        'user', 'guest_session', 'session_start', 'session_duration',
        'actions_performed', 'device_type', 'browser'
    ]
    list_filter = ['session_start', 'device_type', 'browser']
    search_fields = ['user__username', 'guest_session', 'user_agent']
    readonly_fields = ['session_start']
    raw_id_fields = ['user']
    date_hierarchy = 'session_start'
    
    def has_add_permission(self, request):
        return False


@admin.register(LanguageUsage)
class LanguageUsageAdmin(admin.ModelAdmin):
    """Language Usage Admin"""
    list_display = [
        'language_code', 'date', 'translation_requests', 'story_views',
        'game_plays', 'tts_requests', 'unique_users'
    ]
    list_filter = ['language_code', 'date']
    readonly_fields = ['date']
    date_hierarchy = 'date'


@admin.register(FeatureUsage)
class FeatureUsageAdmin(admin.ModelAdmin):
    """Feature Usage Admin"""
    list_display = [
        'feature_name', 'feature_type', 'date', 'total_uses',
        'unique_users', 'success_rate', 'average_response_time'
    ]
    list_filter = ['feature_type', 'date']
    readonly_fields = ['date']
    date_hierarchy = 'date'


@admin.register(ContentPerformance)
class ContentPerformanceAdmin(admin.ModelAdmin):
    """Content Performance Admin"""
    list_display = [
        'content_type', 'content_title', 'date', 'views',
        'likes', 'average_rating', 'average_engagement_time'
    ]
    list_filter = ['content_type', 'date']
    search_fields = ['content_title']
    readonly_fields = ['date']
    date_hierarchy = 'date'


@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    """System Metrics Admin"""
    list_display = [
        'date', 'total_users', 'active_users_daily', 'new_users',
        'total_translations', 'average_response_time', 'uptime_percentage'
    ]
    list_filter = ['date']
    readonly_fields = ['date']
    date_hierarchy = 'date'


@admin.register(UserRetention)
class UserRetentionAdmin(admin.ModelAdmin):
    """User Retention Admin"""
    list_display = [
        'user', 'cohort_week', 'day_1_return', 'day_7_return',
        'day_30_return', 'total_sessions', 'last_activity'
    ]
    list_filter = ['cohort_week', 'day_1_return', 'day_7_return', 'day_30_return']
    search_fields = ['user__username']
    readonly_fields = ['cohort_week', 'last_activity']
    raw_id_fields = ['user']
    date_hierarchy = 'cohort_week'