from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    # path('contacts/', views.ContactView, name='contact_view'),
    path('contacts/', views.ContactViewSet.as_view({'get': 'list', 'post': 'create'}), name='contact_api_view'),
    path('contacts/<int:pk>/', views.ContactViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='contact_api_detail_view'),
    path('contacts/<int:pk>/update/', views.ContactViewSet.as_view({'put': 'update'}), name='contact_api_update_view'),
    path('contacts/<int:pk>/delete/', views.ContactViewSet.as_view({'delete': 'destroy'}), name='contact_api_delete_view'),
]