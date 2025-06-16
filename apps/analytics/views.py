from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta, date
from .models import (
    UserEngagement, LanguageUsage, FeatureUsage,
    ContentPerformance, SystemMetrics, UserRetention
)
from .serializers import (
    UserEngagementSerializer, LanguageUsageSerializer,
    FeatureUsageSerializer, ContentPerformanceSerializer,
    SystemMetricsSerializer, UserRetentionSerializer
)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def dashboard_overview(request):
    """Get dashboard overview statistics"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # User metrics
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    total_users = User.objects.count()
    new_users_today = User.objects.filter(date_joined__date=today).count()
    new_users_week = User.objects.filter(date_joined__date__gte=week_ago).count()
    
    # Activity metrics
    from apps.translations.models import Translation
    from apps.stories.models import Story, StoryInteraction
    from apps.games.models import GameSession
    
    total_translations = Translation.objects.count()
    translations_today = Translation.objects.filter(created_at__date=today).count()
    
    total_stories = Story.objects.filter(is_published=True).count()
    story_views_today = StoryInteraction.objects.filter(
        interaction_type='view',
        timestamp__date=today
    ).count()
    
    games_played_today = GameSession.objects.filter(
        started_at__date=today,
        completed=True
    ).count()
    
    # Language usage
    language_stats = {}
    for lang_usage in LanguageUsage.objects.filter(date=today):
        language_stats[lang_usage.language_code] = {
            'translations': lang_usage.translation_requests,
            'stories': lang_usage.story_views,
            'games': lang_usage.game_plays,
            'tts': lang_usage.tts_requests,
        }
    
    # Engagement metrics
    avg_session_duration = UserEngagement.objects.filter(
        session_start__date=today,
        session_duration__isnull=False
    ).aggregate(avg_duration=Avg('session_duration'))['avg_duration'] or 0
    
    return Response({
        'users': {
            'total': total_users,
            'new_today': new_users_today,
            'new_this_week': new_users_week,
        },
        'activity': {
            'total_translations': total_translations,
            'translations_today': translations_today,
            'total_stories': total_stories,
            'story_views_today': story_views_today,
            'games_played_today': games_played_today,
        },
        'engagement': {
            'avg_session_duration': round(avg_session_duration / 60, 2) if avg_session_duration else 0,  # in minutes
        },
        'languages': language_stats,
        'date': today,
    })


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def language_analytics(request):
    """Get language usage analytics"""
    days = int(request.query_params.get('days', 30))
    start_date = timezone.now().date() - timedelta(days=days)
    
    language_data = LanguageUsage.objects.filter(
        date__gte=start_date
    ).order_by('date', 'language_code')
    
    # Aggregate data by language
    language_totals = {}
    daily_data = {}
    
    for usage in language_data:
        lang = usage.language_code
        date_str = usage.date.isoformat()
        
        if lang not in language_totals:
            language_totals[lang] = {
                'translations': 0,
                'stories': 0,
                'games': 0,
                'tts': 0,
                'users': 0,
            }
        
        language_totals[lang]['translations'] += usage.translation_requests
        language_totals[lang]['stories'] += usage.story_views
        language_totals[lang]['games'] += usage.game_plays
        language_totals[lang]['tts'] += usage.tts_requests
        language_totals[lang]['users'] += usage.unique_users
        
        if date_str not in daily_data:
            daily_data[date_str] = {}
        
        daily_data[date_str][lang] = {
            'translations': usage.translation_requests,
            'stories': usage.story_views,
            'games': usage.game_plays,
            'tts': usage.tts_requests,
        }
    
    return Response({
        'totals': language_totals,
        'daily': daily_data,
        'period': f"{days} days",
    })


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def feature_analytics(request):
    """Get feature usage analytics"""
    days = int(request.query_params.get('days', 30))
    start_date = timezone.now().date() - timedelta(days=days)
    
    feature_data = FeatureUsage.objects.filter(
        date__gte=start_date
    ).order_by('feature_name', 'date')
    
    # Aggregate by feature
    feature_totals = {}
    for usage in feature_data:
        feature = usage.feature_name
        if feature not in feature_totals:
            feature_totals[feature] = {
                'type': usage.feature_type,
                'total_uses': 0,
                'unique_users': 0,
                'avg_session_time': 0,
                'success_rate': 0,
                'avg_response_time': 0,
                'days_count': 0,
            }
        
        feature_totals[feature]['total_uses'] += usage.total_uses
        feature_totals[feature]['unique_users'] += usage.unique_users
        feature_totals[feature]['avg_session_time'] += usage.average_session_time
        feature_totals[feature]['success_rate'] += usage.success_rate
        feature_totals[feature]['avg_response_time'] += usage.average_response_time
        feature_totals[feature]['days_count'] += 1
    
    # Calculate averages
    for feature in feature_totals:
        days_count = feature_totals[feature]['days_count']
        if days_count > 0:
            feature_totals[feature]['avg_session_time'] /= days_count
            feature_totals[feature]['success_rate'] /= days_count
            feature_totals[feature]['avg_response_time'] /= days_count
        del feature_totals[feature]['days_count']
    
    return Response({
        'features': feature_totals,
        'period': f"{days} days",
    })


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def content_analytics(request):
    """Get content performance analytics"""
    content_type = request.query_params.get('type', 'all')
    days = int(request.query_params.get('days', 30))
    start_date = timezone.now().date() - timedelta(days=days)
    
    queryset = ContentPerformance.objects.filter(date__gte=start_date)
    
    if content_type != 'all':
        queryset = queryset.filter(content_type=content_type)
    
    # Top performing content
    top_content = queryset.values(
        'content_type', 'content_id', 'content_title'
    ).annotate(
        total_views=Sum('views'),
        total_likes=Sum('likes'),
        total_shares=Sum('shares'),
        avg_rating=Avg('average_rating'),
        avg_engagement=Avg('average_engagement_time')
    ).order_by('-total_views')[:10]
    
    # Content type breakdown
    type_breakdown = queryset.values('content_type').annotate(
        total_views=Sum('views'),
        total_likes=Sum('likes'),
        total_completions=Sum('completions'),
        avg_rating=Avg('average_rating')
    ).order_by('-total_views')
    
    return Response({
        'top_content': list(top_content),
        'type_breakdown': list(type_breakdown),
        'period': f"{days} days",
    })


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def user_retention_analytics(request):
    """Get user retention analytics"""
    weeks = int(request.query_params.get('weeks', 12))
    start_date = timezone.now().date() - timedelta(weeks=weeks)
    
    retention_data = UserRetention.objects.filter(
        cohort_week__gte=start_date
    ).order_by('cohort_week')
    
    # Calculate retention rates by cohort
    cohort_stats = {}
    for retention in retention_data:
        week = retention.cohort_week.isoformat()
        if week not in cohort_stats:
            cohort_stats[week] = {
                'total_users': 0,
                'day_1_retained': 0,
                'day_7_retained': 0,
                'day_30_retained': 0,
            }
        
        cohort_stats[week]['total_users'] += 1
        if retention.day_1_return:
            cohort_stats[week]['day_1_retained'] += 1
        if retention.day_7_return:
            cohort_stats[week]['day_7_retained'] += 1
        if retention.day_30_return:
            cohort_stats[week]['day_30_retained'] += 1
    
    # Calculate retention percentages
    for week in cohort_stats:
        total = cohort_stats[week]['total_users']
        if total > 0:
            cohort_stats[week]['day_1_rate'] = (cohort_stats[week]['day_1_retained'] / total) * 100
            cohort_stats[week]['day_7_rate'] = (cohort_stats[week]['day_7_retained'] / total) * 100
            cohort_stats[week]['day_30_rate'] = (cohort_stats[week]['day_30_retained'] / total) * 100
    
    return Response({
        'cohorts': cohort_stats,
        'period': f"{weeks} weeks",
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def track_engagement(request):
    """Track user engagement event"""
    engagement_data = {
        'pages_visited': request.data.get('pages_visited', []),
        'features_used': request.data.get('features_used', []),
        'actions_performed': request.data.get('actions_performed', 0),
        'session_duration': request.data.get('session_duration'),
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'ip_address': request.META.get('REMOTE_ADDR'),
        'device_type': request.data.get('device_type', ''),
        'browser': request.data.get('browser', ''),
    }
    
    if request.user.is_authenticated:
        engagement_data['user'] = request.user
    else:
        guest_session = request.session.get('guest_id')
        if not guest_session:
            import uuid
            guest_session = str(uuid.uuid4())
            request.session['guest_id'] = guest_session
        engagement_data['guest_session'] = guest_session
    
    UserEngagement.objects.create(**engagement_data)
    
    return Response({'message': 'Engagement tracked successfully'})


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def export_analytics(request):
    """Export analytics data"""
    export_type = request.query_params.get('type', 'overview')
    days = int(request.query_params.get('days', 30))
    start_date = timezone.now().date() - timedelta(days=days)
    
    if export_type == 'users':
        data = UserEngagement.objects.filter(
            session_start__date__gte=start_date
        ).values(
            'user__username', 'session_start', 'session_duration',
            'actions_performed', 'device_type', 'browser'
        )
    elif export_type == 'languages':
        data = LanguageUsage.objects.filter(
            date__gte=start_date
        ).values()
    elif export_type == 'features':
        data = FeatureUsage.objects.filter(
            date__gte=start_date
        ).values()
    elif export_type == 'content':
        data = ContentPerformance.objects.filter(
            date__gte=start_date
        ).values()
    else:
        return Response(
            {'error': 'Invalid export type'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({
        'data': list(data),
        'type': export_type,
        'period': f"{days} days",
        'exported_at': timezone.now(),
    })