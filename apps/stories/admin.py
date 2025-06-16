from django.contrib import admin
from .models import Story, StoryInteraction, StoryCollection, StoryRating


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    """Story Admin"""
    list_display = [
        'title', 'language', 'category', 'difficulty', 'views', 'likes',
        'featured', 'is_published', 'created_at'
    ]
    list_filter = [
        'language', 'category', 'difficulty', 'featured', 'is_published', 'created_at'
    ]
    search_fields = ['title', 'content', 'author', 'cultural_origin']
    readonly_fields = ['views', 'likes', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content', 'summary', 'author', 'source')
        }),
        ('Classification', {
            'fields': ('language', 'cultural_origin', 'category', 'difficulty')
        }),
        ('Media', {
            'fields': ('audio_url', 'image_url')
        }),
        ('Publishing', {
            'fields': ('is_published', 'featured')
        }),
        ('Metrics', {
            'fields': ('views', 'likes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_featured', 'remove_featured', 'publish_stories', 'unpublish_stories']
    
    def make_featured(self, request, queryset):
        queryset.update(featured=True)
    make_featured.short_description = "Mark selected stories as featured"
    
    def remove_featured(self, request, queryset):
        queryset.update(featured=False)
    remove_featured.short_description = "Remove featured status"
    
    def publish_stories(self, request, queryset):
        queryset.update(is_published=True)
    publish_stories.short_description = "Publish selected stories"
    
    def unpublish_stories(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_stories.short_description = "Unpublish selected stories"


@admin.register(StoryInteraction)
class StoryInteractionAdmin(admin.ModelAdmin):
    """Story Interaction Admin"""
    list_display = ['story', 'user', 'interaction_type', 'timestamp']
    list_filter = ['interaction_type', 'timestamp']
    search_fields = ['story__title', 'user__username']
    readonly_fields = ['timestamp']
    raw_id_fields = ['user', 'story']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False


@admin.register(StoryCollection)
class StoryCollectionAdmin(admin.ModelAdmin):
    """Story Collection Admin"""
    list_display = ['name', 'is_featured', 'created_by', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['stories']
    readonly_fields = ['created_at']


@admin.register(StoryRating)
class StoryRatingAdmin(admin.ModelAdmin):
    """Story Rating Admin"""
    list_display = ['story', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['story__title', 'user__username', 'review']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['user', 'story']