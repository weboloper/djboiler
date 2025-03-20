from django.urls import path,include
# from . import views
from . import views

app_name = 'posts'

urlpatterns = [
    path('api/posts/', include('posts.api.urls')),
]