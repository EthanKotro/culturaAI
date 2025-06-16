from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import UserPreferences, UserActivity
from .serializers import (
    UserSerializer, UserPreferencesSerializer, 
    UserActivitySerializer, UserProfileSerializer
)

User = get_user_model()


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserPreferencesView(generics.RetrieveUpdateAPIView):
    """Get and update user preferences"""
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        preferences, created = UserPreferences.objects.get_or_create(
            user=self.request.user
        )
        return preferences


class UserActivitiesView(generics.ListCreateAPIView):
    """List user activities and create new ones"""
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user)[:50]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_points(request):
    """Add points to user account"""
    points = request.data.get('points', 0)
    activity_type = request.data.get('activity_type', 'general')
    
    if points > 0:
        request.user.add_points(points)
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            activity_type=activity_type,
            activity_data={'points_earned': points}
        )
        
        return Response({
            'message': f'Added {points} points',
            'total_points': request.user.points,
            'level': request.user.level
        })
    
    return Response(
        {'error': 'Invalid points value'}, 
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def guest_user(request):
    """Create or get guest user session"""
    # For guest users, we'll use session-based identification
    guest_id = request.session.get('guest_id')
    
    if not guest_id:
        # Create a new guest session
        import uuid
        guest_id = str(uuid.uuid4())
        request.session['guest_id'] = guest_id
        request.session['is_guest'] = True
    
    return Response({
        'guest_id': guest_id,
        'is_guest': True,
        'message': 'Guest session created'
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Get user statistics"""
    user = request.user
    
    # Calculate additional stats
    recent_activities = UserActivity.objects.filter(user=user).count()
    
    stats = {
        'points': user.points,
        'level': user.level,
        'learning_streak': user.learning_streak,
        'total_translations': user.total_translations,
        'total_stories_read': user.total_stories_read,
        'total_games_played': user.total_games_played,
        'recent_activities': recent_activities,
        'member_since': user.date_joined.strftime('%B %Y'),
        'last_active': user.last_active,
    }
    
    return Response(stats)