from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserPreferences, UserActivity

# Unregister the default UserAdmin
# admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    """Enhanced User Admin"""
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'is_staff', 'is_superuser', 'is_active', 'date_joined'
    ]
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'date_joined'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Firebase Info', {
            'fields': ('firebase_uid',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # readonly_fields = ['firebase_uid', 'date_joined', 'last_login']

# Register the custom admin class
admin.site.register(User, CustomUserAdmin)


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    """User Preferences Admin"""
    # list_display = ('user', 'theme', 'notifications_enabled')
    search_fields = ('user__username',)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """User Activity Admin"""
    list_display = ['user', 'activity_type', 'timestamp']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__username', 'user__email', 'activity_type']
    raw_id_fields = ['user']
    # readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False  # Activities are created programmatically