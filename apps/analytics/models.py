from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class UserEngagement(models.Model):
    """Track user engagement metrics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_session = models.CharField(max_length=100, null=True, blank=True)
    
    # Session data
    session_start = models.DateTimeField(auto_now_add=True)
    session_end = models.DateTimeField(null=True, blank=True)
    session_duration = models.IntegerField(null=True, blank=True)  # in seconds
    
    # Activity data
    pages_visited = models.JSONField(default=list)
    features_used = models.JSONField(default=list)
    actions_performed = models.IntegerField(default=0)
    
    # Device and location
    user_agent = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_type = models.CharField(max_length=50, blank=True)
    browser = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'user_engagement'
        ordering = ['-session_start']
        indexes = [
            models.Index(fields=['user', '-session_start']),
            models.Index(fields=['session_start']),
        ]
    
    def __str__(self):
        return f"{self.user or self.guest_session} - {self.session_start}"


class LanguageUsage(models.Model):
    """Track language usage patterns"""
    language_code = models.CharField(max_length=10)
    
    # Usage metrics
    translation_requests = models.IntegerField(default=0)
    story_views = models.IntegerField(default=0)
    game_plays = models.IntegerField(default=0)
    tts_requests = models.IntegerField(default=0)
    
    # Time-based tracking
    date = models.DateField(default=timezone.now)
    
    # User segmentation
    unique_users = models.IntegerField(default=0)
    guest_users = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'language_usage'
        unique_together = ['language_code', 'date']
        ordering = ['-date', 'language_code']
    
    def __str__(self):
        return f"{self.language_code} - {self.date}"


class FeatureUsage(models.Model):
    """Track feature usage across the platform"""
    FEATURE_TYPES = [
        ('translation', 'Translation'),
        ('stories', 'Stories'),
        ('games', 'Games'),
        ('tts', 'Text-to-Speech'),
        ('profile', 'User Profile'),
        ('settings', 'Settings'),
    ]
    
    feature_name = models.CharField(max_length=50)
    feature_type = models.CharField(max_length=20, choices=FEATURE_TYPES)
    
    # Usage metrics
    total_uses = models.IntegerField(default=0)
    unique_users = models.IntegerField(default=0)
    average_session_time = models.FloatField(default=0.0)
    
    # Performance metrics
    success_rate = models.FloatField(default=0.0)
    error_rate = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    
    # Time tracking
    date = models.DateField(default=timezone.now)
    
    class Meta:
        db_table = 'feature_usage'
        unique_together = ['feature_name', 'date']
        ordering = ['-date', 'feature_name']
    
    def __str__(self):
        return f"{self.feature_name} - {self.date}"


class ContentPerformance(models.Model):
    """Track performance of content (stories, games, etc.)"""
    CONTENT_TYPES = [
        ('story', 'Story'),
        ('game', 'Game'),
        ('translation', 'Translation'),
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_id = models.IntegerField()
    content_title = models.CharField(max_length=200)
    
    # Engagement metrics
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    completions = models.IntegerField(default=0)
    
    # Quality metrics
    average_rating = models.FloatField(default=0.0)
    total_ratings = models.IntegerField(default=0)
    bounce_rate = models.FloatField(default=0.0)
    
    # Time metrics
    average_engagement_time = models.FloatField(default=0.0)
    
    # Date tracking
    date = models.DateField(default=timezone.now)
    
    class Meta:
        db_table = 'content_performance'
        unique_together = ['content_type', 'content_id', 'date']
        ordering = ['-date', 'content_type']
    
    def __str__(self):
        return f"{self.content_type} - {self.content_title} - {self.date}"


class SystemMetrics(models.Model):
    """Track system-wide metrics"""
    # User metrics
    total_users = models.IntegerField(default=0)
    active_users_daily = models.IntegerField(default=0)
    active_users_weekly = models.IntegerField(default=0)
    active_users_monthly = models.IntegerField(default=0)
    new_users = models.IntegerField(default=0)
    
    # Content metrics
    total_translations = models.IntegerField(default=0)
    total_stories = models.IntegerField(default=0)
    total_games_played = models.IntegerField(default=0)
    
    # Performance metrics
    average_response_time = models.FloatField(default=0.0)
    error_rate = models.FloatField(default=0.0)
    uptime_percentage = models.FloatField(default=100.0)
    
    # Date tracking
    date = models.DateField(default=timezone.now)
    
    class Meta:
        db_table = 'system_metrics'
        ordering = ['-date']
    
    def __str__(self):
        return f"System Metrics - {self.date}"


class UserRetention(models.Model):
    """Track user retention metrics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Retention periods
    day_1_return = models.BooleanField(default=False)
    day_7_return = models.BooleanField(default=False)
    day_30_return = models.BooleanField(default=False)
    
    # Activity metrics
    total_sessions = models.IntegerField(default=0)
    total_time_spent = models.IntegerField(default=0)  # in seconds
    features_used_count = models.IntegerField(default=0)
    
    # Engagement quality
    high_engagement_sessions = models.IntegerField(default=0)
    content_created = models.IntegerField(default=0)
    social_interactions = models.IntegerField(default=0)
    
    # Cohort tracking
    cohort_week = models.DateField()
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_retention'
        unique_together = ['user', 'cohort_week']
        ordering = ['-cohort_week', 'user']
    
    def __str__(self):
        return f"{self.user.username} - Cohort {self.cohort_week}"