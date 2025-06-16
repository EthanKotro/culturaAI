from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg, Count
from .models import Story, StoryInteraction, StoryCollection, StoryRating
from .serializers import (
    StorySerializer, StoryListSerializer, StoryInteractionSerializer,
    StoryCollectionSerializer, StoryRatingSerializer
)


class StoryListView(generics.ListAPIView):
    """List stories with filtering"""
    serializer_class = StoryListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Story.objects.filter(is_published=True)
        
        # Filters
        language = self.request.query_params.get('language')
        category = self.request.query_params.get('category')
        difficulty = self.request.query_params.get('difficulty')
        featured = self.request.query_params.get('featured')
        search = self.request.query_params.get('search')
        
        if language:
            queryset = queryset.filter(language=language)
        if category:
            queryset = queryset.filter(category=category)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if featured:
            queryset = queryset.filter(featured=True)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(summary__icontains=search)
            )
        
        return queryset.order_by('-featured', '-views')


class StoryDetailView(generics.RetrieveAPIView):
    """Get story details"""
    serializer_class = StorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Story.objects.filter(is_published=True)
    
    def retrieve(self, request, *args, **kwargs):
        story = self.get_object()
        
        # Increment view count
        story.increment_views()
        
        # Log interaction
        if request.user.is_authenticated:
            StoryInteraction.objects.get_or_create(
                user=request.user,
                story=story,
                interaction_type='view'
            )
        else:
            guest_session = request.session.get('guest_id')
            if guest_session:
                StoryInteraction.objects.get_or_create(
                    guest_session=guest_session,
                    story=story,
                    interaction_type='view'
                )
        
        serializer = self.get_serializer(story)
        return Response(serializer.data)


class StoryCollectionListView(generics.ListAPIView):
    """List story collections"""
    serializer_class = StoryCollectionSerializer
    permission_classes = [permissions.AllowAny]
    queryset = StoryCollection.objects.all()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def interact_with_story(request, story_id):
    """Record story interaction"""
    try:
        story = Story.objects.get(id=story_id, is_published=True)
        interaction_type = request.data.get('interaction_type')
        
        if interaction_type not in ['like', 'share', 'bookmark', 'complete']:
            return Response(
                {'error': 'Invalid interaction type'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        interaction_data = {
            'story': story,
            'interaction_type': interaction_type,
            'reading_time': request.data.get('reading_time'),
            'completion_percentage': request.data.get('completion_percentage'),
        }
        
        if request.user.is_authenticated:
            interaction_data['user'] = request.user
        else:
            guest_session = request.session.get('guest_id')
            if not guest_session:
                import uuid
                guest_session = str(uuid.uuid4())
                request.session['guest_id'] = guest_session
            interaction_data['guest_session'] = guest_session
        
        # Handle like interaction
        if interaction_type == 'like':
            interaction, created = StoryInteraction.objects.get_or_create(
                user=interaction_data.get('user'),
                guest_session=interaction_data.get('guest_session'),
                story=story,
                interaction_type='like'
            )
            
            if created:
                story.likes += 1
                story.save()
                message = 'Story liked'
            else:
                interaction.delete()
                story.likes = max(0, story.likes - 1)
                story.save()
                message = 'Story unliked'
        else:
            StoryInteraction.objects.create(**interaction_data)
            message = f'Interaction recorded: {interaction_type}'
        
        return Response({'message': message})
        
    except Story.DoesNotExist:
        return Response(
            {'error': 'Story not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def rate_story(request, story_id):
    """Rate a story"""
    try:
        story = Story.objects.get(id=story_id, is_published=True)
        rating_value = request.data.get('rating')
        review_text = request.data.get('review', '')
        
        if not rating_value or not (1 <= int(rating_value) <= 5):
            return Response(
                {'error': 'Rating must be between 1 and 5'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rating_data = {
            'story': story,
            'rating': int(rating_value),
            'review': review_text,
        }
        
        if request.user.is_authenticated:
            rating_data['user'] = request.user
            rating, created = StoryRating.objects.update_or_create(
                user=request.user,
                story=story,
                defaults=rating_data
            )
        else:
            guest_session = request.session.get('guest_id')
            if not guest_session:
                import uuid
                guest_session = str(uuid.uuid4())
                request.session['guest_id'] = guest_session
            
            rating_data['guest_session'] = guest_session
            rating, created = StoryRating.objects.update_or_create(
                guest_session=guest_session,
                story=story,
                defaults=rating_data
            )
        
        message = 'Rating updated' if not created else 'Rating added'
        return Response({'message': message})
        
    except Story.DoesNotExist:
        return Response(
            {'error': 'Story not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def story_stats(request):
    """Get story statistics"""
    stats = {
        'total_stories': Story.objects.filter(is_published=True).count(),
        'stories_by_language': {},
        'stories_by_category': {},
        'most_viewed': [],
        'most_liked': [],
        'featured_stories': Story.objects.filter(featured=True, is_published=True).count()
    }
    
    # Stories by language
    from django.conf import settings
    for lang_code, lang_info in settings.SUPPORTED_LANGUAGES.items():
        if lang_code != 'en':
            count = Story.objects.filter(language=lang_code, is_published=True).count()
            stats['stories_by_language'][lang_code] = {
                'name': lang_info['name'],
                'count': count
            }
    
    # Stories by category
    categories = Story.objects.filter(is_published=True).values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    for cat in categories:
        stats['stories_by_category'][cat['category']] = cat['count']
    
    # Most viewed stories
    most_viewed = Story.objects.filter(is_published=True).order_by('-views')[:5]
    stats['most_viewed'] = StoryListSerializer(most_viewed, many=True).data
    
    # Most liked stories
    most_liked = Story.objects.filter(is_published=True).order_by('-likes')[:5]
    stats['most_liked'] = StoryListSerializer(most_liked, many=True).data
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_stories(request):
    """Get featured stories"""
    featured = Story.objects.filter(featured=True, is_published=True)[:6]
    serializer = StoryListSerializer(featured, many=True)
    return Response(serializer.data)