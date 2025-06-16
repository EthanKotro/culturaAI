from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended User model with Firebase integration"""
    firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=True)
    
    class Meta:
        db_table = 'auth_user_extended'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username or self.email


class UserActivity(models.Model):
    """Track user activities for analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_activities')
    activity_type = models.CharField(max_length=50)
    activity_data = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"


class UserPreferences(models.Model):
    """User preferences and settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_preferences')
    source_language = models.CharField(max_length=10, default='en')
    target_language = models.CharField(max_length=10, default='ki')
    tts_enabled = models.BooleanField(default=True)
    tts_speed = models.FloatField(default=1.0)
    email_notifications = models.BooleanField(default=True)
    learning_reminders = models.BooleanField(default=True)
    profile_public = models.BooleanField(default=False)
    share_progress = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Preferences'
        verbose_name_plural = 'User Preferences'
    
    def __str__(self):
        return f"Preferences for {self.user.username}"