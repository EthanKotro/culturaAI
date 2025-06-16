from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg, Count
from django.utils import timezone
from .models import Game, GameSession, GameLeaderboard, Achievement, UserAchievement
from .serializers import (
    GameSerializer, GameListSerializer, GameSessionSerializer,
    GameLeaderboardSerializer, AchievementSerializer, UserAchievementSerializer
)
import json


class GameListView(generics.ListAPIView):
    """List available games"""
    serializer_class = GameListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Game.objects.filter(is_active=True)
        
        # Filters
        game_type = self.request.query_params.get('type')
        difficulty = self.request.query_params.get('difficulty')
        language = self.request.query_params.get('language')
        featured = self.request.query_params.get('featured')
        
        if game_type:
            queryset = queryset.filter(game_type=game_type)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if language:
            queryset = queryset.filter(
                Q(source_language=language) | Q(target_language=language)
            )
        if featured:
            queryset = queryset.filter(is_featured=True)
        
        return queryset.order_by('-is_featured', 'name')


class GameDetailView(generics.RetrieveAPIView):
    """Get game details"""
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Game.objects.filter(is_active=True)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def start_game(request, game_id):
    """Start a new game session"""
    try:
        game = Game.objects.get(id=game_id, is_active=True)
        
        session_data = {
            'game': game,
            'max_possible_score': game.max_score,
        }
        
        if request.user.is_authenticated:
            session_data['user'] = request.user
        else:
            guest_session = request.session.get('guest_id')
            if not guest_session:
                import uuid
                guest_session = str(uuid.uuid4())
                request.session['guest_id'] = guest_session
            session_data['guest_session'] = guest_session
        
        session = GameSession.objects.create(**session_data)
        
        # Return game data for the frontend
        response_data = {
            'session_id': session.id,
            'game': GameSerializer(game, context={'request': request}).data,
            'game_data': game.game_data,
            'time_limit': game.time_limit,
            'max_score': game.max_score,
            'min_score_to_pass': game.min_score_to_pass,
        }
        
        return Response(response_data)
        
    except Game.DoesNotExist:
        return Response(
            {'error': 'Game not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def submit_game(request, session_id):
    """Submit game results"""
    try:
        session = GameSession.objects.get(id=session_id)
        
        # Verify ownership
        if request.user.is_authenticated:
            if session.user != request.user:
                return Response(
                    {'error': 'Unauthorized'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            guest_session = request.session.get('guest_id')
            if session.guest_session != guest_session:
                return Response(
                    {'error': 'Unauthorized'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Update session with results
        session.score = request.data.get('score', 0)
        session.time_taken = request.data.get('time_taken', 0)
        session.answers = request.data.get('answers', {})
        session.feedback = request.data.get('feedback', {})
        session.completed = True
        session.completed_at = timezone.now()
        session.passed = session.score >= session.game.min_score_to_pass
        session.save()
        
        # Update leaderboard for authenticated users
        if request.user.is_authenticated:
            leaderboard, created = GameLeaderboard.objects.get_or_create(
                game=session.game,
                user=request.user
            )
            leaderboard.update_stats(session)
            
            # Award points
            points_earned = session.score // 10  # 1 point per 10 game points
            if session.passed:
                points_earned += 20  # Bonus for passing
            
            request.user.add_points(points_earned)
            request.user.total_games_played += 1
            request.user.save()
            
            # Check for achievements
            check_achievements(request.user, session)
        
        response_data = {
            'session': GameSessionSerializer(session).data,
            'passed': session.passed,
            'percentage': session.calculate_percentage(),
        }
        
        if request.user.is_authenticated:
            response_data['points_earned'] = points_earned
        
        return Response(response_data)
        
    except GameSession.DoesNotExist:
        return Response(
            {'error': 'Game session not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


class GameSessionListView(generics.ListAPIView):
    """List user's game sessions"""
    serializer_class = GameSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return GameSession.objects.filter(user=self.request.user).order_by('-started_at')


class GameLeaderboardView(generics.ListAPIView):
    """Get game leaderboard"""
    serializer_class = GameLeaderboardSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        game_id = self.kwargs.get('game_id')
        return GameLeaderboard.objects.filter(game_id=game_id).order_by('-best_score', 'best_time')[:50]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def game_stats(request):
    """Get game statistics"""
    stats = {
        'total_games': Game.objects.filter(is_active=True).count(),
        'total_sessions': GameSession.objects.filter(completed=True).count(),
        'games_by_type': {},
        'games_by_difficulty': {},
        'popular_games': [],
        'recent_sessions': []
    }
    
    # Games by type
    game_types = Game.objects.filter(is_active=True).values('game_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    for gt in game_types:
        stats['games_by_type'][gt['game_type']] = gt['count']
    
    # Games by difficulty
    difficulties = Game.objects.filter(is_active=True).values('difficulty').annotate(
        count=Count('id')
    ).order_by('-count')
    
    for diff in difficulties:
        stats['games_by_difficulty'][diff['difficulty']] = diff['count']
    
    # Popular games
    popular = Game.objects.filter(is_active=True).annotate(
        session_count=Count('sessions')
    ).order_by('-session_count')[:5]
    
    stats['popular_games'] = GameListSerializer(popular, many=True).data
    
    # Recent sessions (if user is authenticated)
    if request.user.is_authenticated:
        recent = GameSession.objects.filter(
            user=request.user, completed=True
        ).order_by('-completed_at')[:5]
        stats['recent_sessions'] = GameSessionSerializer(recent, many=True).data
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_achievements(request):
    """Get user achievements"""
    achievements = UserAchievement.objects.filter(user=request.user).order_by('-earned_at')
    serializer = UserAchievementSerializer(achievements, many=True)
    return Response(serializer.data)


def check_achievements(user, session):
    """Check and award achievements based on game session"""
    # High Score Achievement
    if session.score >= session.game.max_score * 0.9:  # 90% or higher
        try:
            achievement = Achievement.objects.get(
                achievement_type='score',
                requirements__game_type=session.game.game_type
            )
            UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement,
                defaults={'game_session': session}
            )
        except Achievement.DoesNotExist:
            pass
    
    # Speed Achievement
    if session.game.time_limit and session.time_taken <= session.game.time_limit * 0.5:
        try:
            achievement = Achievement.objects.get(
                achievement_type='speed',
                requirements__game_type=session.game.game_type
            )
            UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement,
                defaults={'game_session': session}
            )
        except Achievement.DoesNotExist:
            pass
    
    # Completion Achievement
    if session.passed:
        try:
            achievement = Achievement.objects.get(
                achievement_type='completion',
                requirements__difficulty=session.game.difficulty
            )
            UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement,
                defaults={'game_session': session}
            )
        except Achievement.DoesNotExist:
            pass