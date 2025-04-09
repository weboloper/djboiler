"""
URLs mapping for users.
"""
from django.urls import path,include
from . import views

app_name = 'api'

urlpatterns = [
    path('<slug:lookup_value>/', views.PostAPIView.as_view(),{'lookup_type': 'sqid'}, name='post-detail'),
    path('slug/<slug:lookup_value>/', views.PostAPIView.as_view(),{'lookup_type': 'slug'}, name='post-detail-by-slug'),
    
]