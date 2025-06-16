from rest_framework import serializers
from .models import Game, GameSession, GameLeaderboard, Achievement, UserAchievement


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game model"""
    total_players = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()
    user_best_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = [
            'id', 'name', 'description', 'game_type', 'difficulty',
            'time_limit', 'max_score', 'min_score_to_pass',
            'source_language', 'target_language', 'is_featured',
            'total_players', 'average_score', 'user_best_score'
        ]
    
    def get_total_players(self, obj):
        return obj.sessions.values('user', 'guest_session').distinct().count()
    
    def get_average_score(self, obj):
        sessions = obj.sessions.filter(completed=True)
        if sessions.exists():
            return round(sessions.aggregate(avg=models.Avg('score'))['avg'], 1)
        return 0
    
    def get_user_best_score(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            leaderboard = obj.leaderboard.filter(user=request.user).first()
            return leaderboard.best_score if leaderboard else 0
        return 0


class GameListSerializer(serializers.ModelSerializer):
    """Simplified serializer for game lists"""
    total_players = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = [
            'id', 'name', 'description', 'game_type', 'difficulty',
            'time_limit', 'max_score', 'is_featured', 'total_players'
        ]
    
    def get_total_players(self, obj):
        return obj.sessions.values('user', 'guest_session').distinct().count()


class GameSessionSerializer(serializers.ModelSerializer):
    """Serializer for Game Session"""
    game_name = serializers.CharField(source='game.name', read_only=True)
    percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = GameSession
        fields = [
            'id', 'game', 'game_name', 'score', 'max_possible_score',
            'time_taken', 'completed', 'passed', 'percentage',
            'started_at', 'completed_at'
        ]
        read_only_fields = ['id', 'started_at']
    
    def get_percentage(self, obj):
        return obj.calculate_percentage()


class GameLeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Game Leaderboard"""
    username = serializers.CharField(source='user.username', read_only=True)
    user_level = serializers.IntegerField(source='user.level', read_only=True)
    
    class Meta:
        model = GameLeaderboard
        fields = [
            'username', 'user_level', 'best_score', 'best_time',
            'best_percentage', 'total_plays', 'average_score'
        ]


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement"""
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'achievement_type',
            'points_reward', 'icon', 'badge_color'
        ]


class UserAchievementSerializer(serializers.ModelSerializer):
    """Serializer for User Achievement"""
    achievement = AchievementSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ['id', 'achievement', 'earned_at']