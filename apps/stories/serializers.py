from rest_framework import serializers
from .models import Story, StoryInteraction, StoryCollection, StoryRating


class StorySerializer(serializers.ModelSerializer):
    """Serializer for Story model"""
    average_rating = serializers.SerializerMethodField()
    total_ratings = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Story
        fields = [
            'id', 'title', 'content', 'summary', 'language', 'cultural_origin',
            'category', 'difficulty', 'audio_url', 'image_url', 'views', 'likes',
            'author', 'source', 'featured', 'created_at', 'average_rating',
            'total_ratings', 'user_rating'
        ]
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return 0
    
    def get_total_ratings(self, obj):
        return obj.ratings.count()
    
    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = obj.ratings.filter(user=request.user).first()
            return rating.rating if rating else None
        return None


class StoryListSerializer(serializers.ModelSerializer):
    """Simplified serializer for story lists"""
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Story
        fields = [
            'id', 'title', 'summary', 'language', 'category', 'difficulty',
            'image_url', 'views', 'likes', 'featured', 'average_rating'
        ]
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return round(sum(r.rating for r in ratings) / len(ratings), 1)
        return 0


class StoryInteractionSerializer(serializers.ModelSerializer):
    """Serializer for Story Interaction"""
    
    class Meta:
        model = StoryInteraction
        fields = [
            'id', 'story', 'interaction_type', 'timestamp',
            'reading_time', 'completion_percentage'
        ]
        read_only_fields = ['id', 'timestamp']


class StoryCollectionSerializer(serializers.ModelSerializer):
    """Serializer for Story Collection"""
    stories = StoryListSerializer(many=True, read_only=True)
    story_count = serializers.SerializerMethodField()
    
    class Meta:
        model = StoryCollection
        fields = [
            'id', 'name', 'description', 'stories', 'story_count',
            'is_featured', 'created_at'
        ]
    
    def get_story_count(self, obj):
        return obj.stories.count()


class StoryRatingSerializer(serializers.ModelSerializer):
    """Serializer for Story Rating"""
    
    class Meta:
        model = StoryRating
        fields = ['id', 'story', 'rating', 'review', 'created_at']
        read_only_fields = ['id', 'created_at']