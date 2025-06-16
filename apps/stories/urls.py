from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoryListView.as_view(), name='story-list'),
    path('<int:pk>/', views.StoryDetailView.as_view(), name='story-detail'),
    path('collections/', views.StoryCollectionListView.as_view(), name='story-collections'),
    path('<int:story_id>/interact/', views.interact_with_story, name='story-interact'),
    path('<int:story_id>/rate/', views.rate_story, name='story-rate'),
    path('stats/', views.story_stats, name='story-stats'),
    path('featured/', views.featured_stories, name='featured-stories'),
]