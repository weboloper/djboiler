"""
URLs mapping for users.
"""
from django.urls import path,include
from . import views

app_name = 'api'

urlpatterns = [
    path('slug/<slug:slug>/', views.PageAPIView.as_view(), name='page-detail'),
    # path('id/<sqid/', views.PageAPIView.as_view(), name='page-detail-sqid'),
]