from django.urls import path,include
from .views import login_view, logout_view, home_view

app_name = 'users'

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('api/users/', include('users.api.urls')),
]