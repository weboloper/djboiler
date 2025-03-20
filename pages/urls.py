from django.urls import path,include
# from . import views
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('<slug:slug>/', views.page_detail_view, name='page-detail-by-slug'),

    path('api/pages/', include('pages.api.urls')),
]