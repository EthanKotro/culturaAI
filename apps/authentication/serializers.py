from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserPreferences, UserActivity

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'preferred_language', 'points', 'level', 'is_guest', 'profile_picture',
            'learning_streak', 'total_translations', 'total_stories_read', 
            'total_games_played', 'date_joined', 'last_active'
        ]
        read_only_fields = [
            'id', 'points', 'level', 'learning_streak', 'total_translations',
            'total_stories_read', 'total_games_played', 'date_joined', 'last_active'
        ]


class UserPreferencesSerializer(serializers.ModelSerializer):
    """Serializer for User Preferences"""
    
    class Meta:
        model = UserPreferences
        fields = [
            'source_language', 'target_language', 'tts_enabled', 'tts_speed',
            'email_notifications', 'learning_reminders', 'profile_public',
            'share_progress', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for User Activity"""
    
    class Meta:
        model = UserActivity
        fields = ['id', 'activity_type', 'activity_data', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class UserProfileSerializer(serializers.ModelSerializer):
    """Complete user profile serializer"""
    preferences = UserPreferencesSerializer(read_only=True)
    recent_activities = UserActivitySerializer(source='activities', many=True, read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'preferred_language', 'points', 'level', 'is_guest', 'profile_picture',
            'learning_streak', 'total_translations', 'total_stories_read', 
            'total_games_played', 'date_joined', 'last_active', 'preferences',
            'recent_activities'
        ]
        read_only_fields = [
            'id', 'points', 'level', 'learning_streak', 'total_translations',
            'total_stories_read', 'total_games_played', 'date_joined', 'last_active'
        ]