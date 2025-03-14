

from django.urls import path,include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('test-email/', views.test_email_view, name='test_email'),
]