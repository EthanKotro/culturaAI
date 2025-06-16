from django.db import models
from django.utils import timezone


class AIModel(models.Model):
    """AI Model configuration and metadata"""
    MODEL_TYPES = [
        ('translation', 'Translation'),
        ('tts', 'Text-to-Speech'),
        ('asr', 'Automatic Speech Recognition'),
        ('embedding', 'Text Embedding'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    model_path = models.CharField(max_length=500)  # HuggingFace model name or local path
    version = models.CharField(max_length=50, default='1.0')
    
    # Configuration
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    max_input_length = models.IntegerField(default=512)
    supported_languages = models.JSONField(default=list)
    
    # Performance metrics
    average_processing_time = models.FloatField(default=0.0)
    total_requests = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    
    # Metadata
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_models'
        ordering = ['model_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.model_type})"
    
    def update_metrics(self, processing_time, success=True):
        """Update model performance metrics"""
        self.total_requests += 1
        
        # Update average processing time
        if self.average_processing_time == 0:
            self.average_processing_time = processing_time
        else:
            self.average_processing_time = (
                (self.average_processing_time * (self.total_requests - 1) + processing_time) 
                / self.total_requests
            )
        
        # Update success rate
        if success:
            current_successes = self.success_rate * (self.total_requests - 1) / 100
            self.success_rate = ((current_successes + 1) / self.total_requests) * 100
        else:
            current_successes = self.success_rate * (self.total_requests - 1) / 100
            self.success_rate = (current_successes / self.total_requests) * 100
        
        self.save()


class ModelRequest(models.Model):
    """Log of AI model requests for monitoring"""
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='requests')
    
    # Request details
    input_text = models.TextField()
    output_text = models.TextField(blank=True)
    source_language = models.CharField(max_length=10, blank=True)
    target_language = models.CharField(max_length=10, blank=True)
    
    # Performance metrics
    processing_time = models.FloatField()
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    # Metadata
    user_agent = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'model_requests'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['model', '-timestamp']),
            models.Index(fields=['success', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.model.name} request at {self.timestamp}"


class ModelCache(models.Model):
    """Cache for AI model outputs"""
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='cache')
    
    input_hash = models.CharField(max_length=64, unique=True)  # SHA256 hash
    input_text = models.TextField()
    output_text = models.TextField()
    
    # Cache metadata
    hit_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'model_cache'
        indexes = [
            models.Index(fields=['model', 'input_hash']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"Cache for {self.model.name}"
    
    def is_expired(self):
        """Check if cache entry is expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class LanguageModel(models.Model):
    """Language-specific model configurations"""
    language_code = models.CharField(max_length=10)
    language_name = models.CharField(max_length=100)
    
    # Model assignments
    translation_model = models.ForeignKey(
        AIModel, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='translation_languages'
    )
    tts_model = models.ForeignKey(
        AIModel, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='tts_languages'
    )
    asr_model = models.ForeignKey(
        AIModel, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='asr_languages'
    )
    
    # Language-specific settings
    is_supported = models.BooleanField(default=True)
    quality_score = models.FloatField(default=0.0)  # BLEU score or similar
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'language_models'
        unique_together = ['language_code']
    
    def __str__(self):
        return f"{self.language_name} ({self.language_code})"