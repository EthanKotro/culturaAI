from rest_framework import serializers
from .models import (
    UserEngagement, LanguageUsage, FeatureUsage, 
    ContentPerformance, SystemMetrics, UserRetention
)


class UserEngagementSerializer(serializers.ModelSerializer):
    """Serializer for User Engagement"""
    
    class Meta:
        model = UserEngagement
        fields = [
            'id', 'session_start', 'session_end', 'session_duration',
            'pages_visited', 'features_used', 'actions_performed',
            'device_type', 'browser'
        ]


class LanguageUsageSerializer(serializers.ModelSerializer):
    """Serializer for Language Usage"""
    
    class Meta:
        model = LanguageUsage
        fields = [
            'language_code', 'translation_requests', 'story_views',
            'game_plays', 'tts_requests', 'unique_users', 'guest_users', 'date'
        ]


class FeatureUsageSerializer(serializers.ModelSerializer):
    """Serializer for Feature Usage"""
    
    class Meta:
        model = FeatureUsage
        fields = [
            'feature_name', 'feature_type', 'total_uses', 'unique_users',
            'average_session_time', 'success_rate', 'error_rate',
            'average_response_time', 'date'
        ]


class ContentPerformanceSerializer(serializers.ModelSerializer):
    """Serializer for Content Performance"""
    
    class Meta:
        model = ContentPerformance
        fields = [
            'content_type', 'content_id', 'content_title', 'views',
            'likes', 'shares', 'completions', 'average_rating',
            'total_ratings', 'bounce_rate', 'average_engagement_time', 'date'
        ]


class SystemMetricsSerializer(serializers.ModelSerializer):
    """Serializer for System Metrics"""
    
    class Meta:
        model = SystemMetrics
        fields = [
            'total_users', 'active_users_daily', 'active_users_weekly',
            'active_users_monthly', 'new_users', 'total_translations',
            'total_stories', 'total_games_played', 'average_response_time',
            'error_rate', 'uptime_percentage', 'date'
        ]


class UserRetentionSerializer(serializers.ModelSerializer):
    """Serializer for User Retention"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserRetention
        fields = [
            'username', 'day_1_return', 'day_7_return', 'day_30_return',
            'total_sessions', 'total_time_spent', 'features_used_count',
            'high_engagement_sessions', 'cohort_week', 'last_activity'
        ]