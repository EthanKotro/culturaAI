from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('preferences/', views.UserPreferencesView.as_view(), name='user-preferences'),
    path('activities/', views.UserActivitiesView.as_view(), name='user-activities'),
    path('add-points/', views.add_points, name='add-points'),
    path('guest/', views.guest_user, name='guest-user'),
    path('stats/', views.user_stats, name='user-stats'),
]