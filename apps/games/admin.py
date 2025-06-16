from django.contrib import admin
from .models import Game, GameSession, GameLeaderboard, Achievement, UserAchievement


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Game Admin"""
    list_display = [
        'name', 'game_type', 'difficulty', 'source_language', 'target_language',
        'max_score', 'is_active', 'is_featured', 'created_at'
    ]
    list_filter = [
        'game_type', 'difficulty', 'source_language', 'target_language',
        'is_active', 'is_featured', 'created_at'
    ]
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'game_type', 'difficulty')
        }),
        ('Configuration', {
            'fields': ('time_limit', 'max_score', 'min_score_to_pass')
        }),
        ('Languages', {
            'fields': ('source_language', 'target_language')
        }),
        ('Game Data', {
            'fields': ('game_data',),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('is_active', 'is_featured', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_featured', 'remove_featured', 'activate_games', 'deactivate_games']
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = "Mark selected games as featured"
    
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
    remove_featured.short_description = "Remove featured status"
    
    def activate_games(self, request, queryset):
        queryset.update(is_active=True)
    activate_games.short_description = "Activate selected games"
    
    def deactivate_games(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_games.short_description = "Deactivate selected games"


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    """Game Session Admin"""
    list_display = [
        'game', 'user', 'score', 'max_possible_score', 'time_taken',
        'completed', 'passed', 'started_at'
    ]
    list_filter = ['completed', 'passed', 'game__game_type', 'started_at']
    search_fields = ['game__name', 'user__username']
    readonly_fields = ['started_at', 'completed_at']
    raw_id_fields = ['user', 'game']
    date_hierarchy = 'started_at'
    
    def has_add_permission(self, request):
        return False


@admin.register(GameLeaderboard)
class GameLeaderboardAdmin(admin.ModelAdmin):
    """Game Leaderboard Admin"""
    list_display = [
        'game', 'user', 'best_score', 'best_time', 'total_plays',
        'average_score', 'last_played'
    ]
    list_filter = ['game__game_type', 'last_played']
    search_fields = ['game__name', 'user__username']
    readonly_fields = ['first_played', 'last_played']
    raw_id_fields = ['user', 'game']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Achievement Admin"""
    list_display = [
        'name', 'achievement_type', 'points_reward', 'icon',
        'badge_color', 'is_active', 'created_at'
    ]
    list_filter = ['achievement_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    """User Achievement Admin"""
    list_display = ['user', 'achievement', 'earned_at']
    list_filter = ['achievement__achievement_type', 'earned_at']
    search_fields = ['user__username', 'achievement__name']
    readonly_fields = ['earned_at']
    raw_id_fields = ['user', 'achievement', 'game_session']
    
    def has_add_permission(self, request):
        return False