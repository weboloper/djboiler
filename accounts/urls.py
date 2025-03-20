from django.urls import path,include
# from . import views
from .views import auth_views,email_views,password_views,oauth_views

app_name = 'accounts'

urlpatterns = [
    path("accounts/", include([
        # auth urls
        path('login/', auth_views.login_view, name='login'),
        path('logout/', auth_views.logout_view, name='logout'),
        path('register/', auth_views.register_view, name='register'),

        # password urls
        path("password/", include([
            path('reset/', password_views.password_reset_request_view, name='password-reset-request'),
            path('reset/<uidb64>/<token>/', password_views.password_reset_confirm_view, name='password-reset-confirm'),
            path('change/', password_views.password_change_view, name='password-change'),
        ])),

        # email urls
        path("email/", include([
            path('verify/', email_views.email_verify_view, name='email-verify-request'),
            path('verify/<uidb64>/<token>/', email_views.email_verify_confirm_view, name='email-verify-confirm'),
            path('change/', email_views.email_change_view, name='email_change_request'),
            path('change/<uidb64>/<token>/', email_views.email_change_confirm_view, name='email-change-confirm'),
        ])),
        
        # oauth urls
        path('auth-receiver', oauth_views.auth_receiver, name='auth-receiver'), # google login
    ])),

    path('api/accounts/', include('accounts.api.urls')),
]