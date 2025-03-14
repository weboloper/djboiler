from django.urls import path,include
from . import views

app_name = 'accounts'

urlpatterns = [

    path("accounts/", include([
        path('login/', views.login_view, name='login'),
        path('logout/', views.logout_view, name='logout'),
        path('register/', views.register_view, name='register'),
        path('test-email/', views.test_email_view, name='test_email'),

        # password urls
        path("password/", include([
            path('reset/', views.password_reset_request_view, name='password_reset_request'),
            path('reset/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
            path('change/', views.password_change_view, name='password_change'),
        ])),

        # email urls
        path("email/", include([
            path('verify/', views.email_verify_view, name='email_verify_request'),
            path('verify/<uidb64>/<token>/', views.email_verify_confirm_view, name='email_verify_confirm'),
            path('change/', views.email_change_view, name='email_change_request'),
            path('change/<uidb64>/<token>/', views.email_change_confirm_view, name='email_change_confirm'),
        ])),
        
        path('auth-receiver', views.auth_receiver, name='auth_receiver'), # google login
    ])),

    path('api/accounts/', include('accounts.api.urls')),
]