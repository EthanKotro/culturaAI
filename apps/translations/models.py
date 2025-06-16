from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Translation(models.Model):
    """Translation model to store translation requests and results"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_session = models.CharField(max_length=100, null=True, blank=True)
    
    source_text = models.TextField()
    translated_text = models.TextField()
    source_language = models.CharField(max_length=10)
    target_language = models.CharField(max_length=10)
    
    # AI model information
    model_used = models.CharField(max_length=100, default='nllb-200')
    confidence_score = models.FloatField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    
    # Quality metrics
    user_rating = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    is_favorite = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'translations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['source_language', 'target_language']),
            models.Index(fields=['guest_session', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.source_language} → {self.target_language}: {self.source_text[:50]}..."


class TranslationFeedback(models.Model):
    """User feedback on translations"""
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Feedback types
    FEEDBACK_TYPES = [
        ('correction', 'Correction'),
        ('rating', 'Rating'),
        ('report', 'Report Issue'),
        ('suggestion', 'Suggestion'),
    ]
    
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    feedback_text = models.TextField()
    suggested_translation = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'translation_feedback'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.feedback_type} for translation {self.translation.id}"


class LanguagePair(models.Model):
    """Language pair configuration and statistics"""
    source_language = models.CharField(max_length=10)
    target_language = models.CharField(max_length=10)
    
    # Statistics
    total_translations = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    average_processing_time = models.FloatField(default=0.0)
    
    # Configuration
    is_active = models.BooleanField(default=True)
    model_name = models.CharField(max_length=100, default='nllb-200')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'language_pairs'
        unique_together = ['source_language', 'target_language']
    
    def __str__(self):
        return f"{self.source_language} → {self.target_language}"
    
    def update_statistics(self):
        """Update statistics based on translations"""
        translations = Translation.objects.filter(
            source_language=self.source_language,
            target_language=self.target_language
        )
        
        self.total_translations = translations.count()
        
        if self.total_translations > 0:
            # Calculate average rating
            rated_translations = translations.filter(user_rating__isnull=False)
            if rated_translations.exists():
                self.average_rating = rated_translations.aggregate(
                    avg_rating=models.Avg('user_rating')
                )['avg_rating']
            
            # Calculate average processing time
            timed_translations = translations.filter(processing_time__isnull=False)
            if timed_translations.exists():
                self.average_processing_time = timed_translations.aggregate(
                    avg_time=models.Avg('processing_time')
                )['avg_time']
        
        self.save()


class TranslationCache(models.Model):
    """Cache frequently requested translations"""
    source_text_hash = models.CharField(max_length=64, unique=True)  # SHA256 hash
    source_text = models.TextField()
    translated_text = models.TextField()
    source_language = models.CharField(max_length=10)
    target_language = models.CharField(max_length=10)
    
    # Cache metadata
    hit_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'translation_cache'
        indexes = [
            models.Index(fields=['source_language', 'target_language']),
            models.Index(fields=['last_accessed']),
        ]
    
    def __str__(self):
        return f"Cached: {self.source_language} → {self.target_language}"