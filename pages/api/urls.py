"""
URLs mapping for users.
"""
from django.urls import path,include
from . import views

app_name = 'api'

urlpatterns = [
    path('<slug:lookup_value>/', views.PageAPIView.as_view(),{'lookup_type': 'sqid'}, name='page-detail'),
    path('slug/<slug:lookup_value>/', views.PageAPIView.as_view(),{'lookup_type': 'slug'}, name='page-detail'),
    
]