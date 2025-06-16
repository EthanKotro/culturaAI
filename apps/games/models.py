from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Game(models.Model):
    """Language learning games"""
    GAME_TYPES = [
        ('word_match', 'Word Match'),
        ('translation_quiz', 'Translation Quiz'),
        ('pronunciation', 'Pronunciation Practice'),
        ('story_builder', 'Story Builder'),
        ('cultural_quiz', 'Cultural Quiz'),
        ('grammar_challenge', 'Grammar Challenge'),
        ('speed_translation', 'Speed Translation'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    game_type = models.CharField(max_length=20, choices=GAME_TYPES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    
    # Game configuration
    time_limit = models.IntegerField(help_text="Time limit in seconds", null=True, blank=True)
    max_score = models.IntegerField(default=100)
    min_score_to_pass = models.IntegerField(default=60)
    
    # Language settings
    source_language = models.CharField(max_length=10)
    target_language = models.CharField(max_length=10)
    
    # Game data
    game_data = models.JSONField(default=dict, help_text="Game questions, options, etc.")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'games'
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['game_type', 'difficulty']),
            models.Index(fields=['source_language', 'target_language']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.game_type})"


class GameSession(models.Model):
    """Individual game play sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_session = models.CharField(max_length=100, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sessions')
    
    # Session data
    score = models.IntegerField(default=0)
    max_possible_score = models.IntegerField(default=100)
    time_taken = models.IntegerField(help_text="Time taken in seconds")
    completed = models.BooleanField(default=False)
    passed = models.BooleanField(default=False)
    
    # Detailed results
    answers = models.JSONField(default=dict, help_text="User answers and correctness")
    feedback = models.JSONField(default=dict, help_text="Detailed feedback")
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'game_sessions'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', '-started_at']),
            models.Index(fields=['game', '-started_at']),
        ]
    
    def __str__(self):
        return f"{self.user or self.guest_session} - {self.game.name} - {self.score}"
    
    def calculate_percentage(self):
        """Calculate score percentage"""
        if self.max_possible_score > 0:
            return (self.score / self.max_possible_score) * 100
        return 0


class GameLeaderboard(models.Model):
    """Leaderboard for games"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='leaderboard')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Best scores
    best_score = models.IntegerField(default=0)
    best_time = models.IntegerField(help_text="Best time in seconds")
    best_percentage = models.FloatField(default=0.0)
    
    # Statistics
    total_plays = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    
    # Timestamps
    first_played = models.DateTimeField(auto_now_add=True)
    last_played = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'game_leaderboard'
        unique_together = ['game', 'user']
        ordering = ['-best_score', 'best_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.game.name} - {self.best_score}"
    
    def update_stats(self, session):
        """Update leaderboard stats from a game session"""
        self.total_plays += 1
        self.total_score += session.score
        self.average_score = self.total_score / self.total_plays
        
        if session.score > self.best_score:
            self.best_score = session.score
            self.best_percentage = session.calculate_percentage()
        
        if not self.best_time or session.time_taken < self.best_time:
            self.best_time = session.time_taken
        
        self.save()


class Achievement(models.Model):
    """Game achievements and badges"""
    ACHIEVEMENT_TYPES = [
        ('score', 'High Score'),
        ('streak', 'Winning Streak'),
        ('completion', 'Game Completion'),
        ('speed', 'Speed Achievement'),
        ('accuracy', 'Accuracy Achievement'),
        ('dedication', 'Dedication Achievement'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    
    # Requirements
    requirements = models.JSONField(default=dict, help_text="Achievement requirements")
    points_reward = models.IntegerField(default=0)
    
    # Display
    icon = models.CharField(max_length=10, default='🏆')
    badge_color = models.CharField(max_length=20, default='gold')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'achievements'
        ordering = ['achievement_type', 'name']
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """User earned achievements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    
    earned_at = models.DateTimeField(auto_now_add=True)
    game_session = models.ForeignKey(GameSession, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'user_achievements'
        unique_together = ['user', 'achievement']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"