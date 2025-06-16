from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Story(models.Model):
    """Traditional African folktales and stories"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    CATEGORY_CHOICES = [
        ('wisdom', 'Wisdom Tales'),
        ('heroic', 'Heroic Tales'),
        ('origin', 'Origin Stories'),
        ('romance', 'Romance'),
        ('humor', 'Humor'),
        ('moral', 'Moral Stories'),
        ('adventure', 'Adventure'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(max_length=500, blank=True)
    
    # Language and cultural information
    language = models.CharField(max_length=10)
    cultural_origin = models.CharField(max_length=100, blank=True)
    
    # Classification
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    
    # Media
    audio_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    
    # Engagement metrics
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    # Metadata
    author = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=200, blank=True)
    is_published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stories'
        ordering = ['-featured', '-created_at']
        indexes = [
            models.Index(fields=['language', 'category']),
            models.Index(fields=['difficulty', 'is_published']),
            models.Index(fields=['-views']),
        ]
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])


class StoryInteraction(models.Model):
    """Track user interactions with stories"""
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('like', 'Like'),
        ('share', 'Share'),
        ('bookmark', 'Bookmark'),
        ('complete', 'Complete Reading'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_session = models.CharField(max_length=100, null=True, blank=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='interactions')
    
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Additional data
    reading_time = models.IntegerField(null=True, blank=True)  # in seconds
    completion_percentage = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'story_interactions'
        unique_together = ['user', 'story', 'interaction_type']
        indexes = [
            models.Index(fields=['story', 'interaction_type']),
            models.Index(fields=['user', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user or self.guest_session} - {self.interaction_type} - {self.story.title}"


class StoryCollection(models.Model):
    """Curated collections of stories"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    stories = models.ManyToManyField(Story, related_name='collections')
    
    # Metadata
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'story_collections'
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.name


class StoryRating(models.Model):
    """User ratings for stories"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_session = models.CharField(max_length=100, null=True, blank=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='ratings')
    
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    review = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'story_ratings'
        unique_together = ['user', 'story']
        indexes = [
            models.Index(fields=['story', 'rating']),
        ]
    
    def __str__(self):
        return f"{self.story.title} - {self.rating} stars"