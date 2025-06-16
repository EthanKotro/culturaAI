from django.urls import path
from . import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='game-list'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),
    path('<int:game_id>/start/', views.start_game, name='start-game'),
    path('sessions/<int:session_id>/submit/', views.submit_game, name='submit-game'),
    path('sessions/', views.GameSessionListView.as_view(), name='game-sessions'),
    path('<int:game_id>/leaderboard/', views.GameLeaderboardView.as_view(), name='game-leaderboard'),
    path('stats/', views.game_stats, name='game-stats'),
    path('achievements/', views.user_achievements, name='user-achievements'),
]