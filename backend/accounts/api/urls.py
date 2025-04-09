"""
URLs mapping for users.
"""
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
# from . import views
from .views import auth_views,email_views,password_views,oauth_views

app_name = 'api'

urlpatterns = [
    # simple jwt defaults
    path("token/", include([
        path('', TokenObtainPairView.as_view(), name='token-obtain-pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
        path('verify/', TokenVerifyView.as_view(), name='token-verify' ),

    ])),

    path('register/', auth_views.RegisterAPIView.as_view(), name='register'),
    path('me/', auth_views.CurrentUserAPIView.as_view(), name='me'),

    # password urls
    path("password/", include([
        path('reset/', password_views.ResetPasswordRequestAPIView.as_view(), name='password-reset-request'),
        path('reset/<uidb64>/<token>/', password_views.ResetPasswordConfirmAPIView.as_view(), name='password-reset-confirm'),
        path('change/', password_views.ChangePasswordAPIView.as_view(), name='password-change'),

    ])),

    # email urls
    path("email/", include([
        path('verify/', email_views.EmailVerificationRequestAPIView.as_view(), name='email-verify-request'),
        path('verify/<uidb64>/<token>/', email_views.EmailVerificationConfirmAPIView.as_view(), name='email-verify-confirm'),
        path('change/', email_views.EmailChangeRequestView.as_view(), name='email-change-request'),
        path('change/<uidb64>/<token>/', email_views.EmailChangeConfirmView.as_view(), name='email-change-confirm'),
    ])),

    path('google-auth/', oauth_views.GoogleAuth.as_view(), name='google-auth'),
    path('google-auth-callback/', oauth_views.GoogleAuthCallback.as_view(), name='google-auth-callback'),  # add path for google authentication
    

    # customs
    # path('current_user/', CurrentUserAPIView.as_view(), name='current_user'),
    # path('register/', RegisterAPIView.as_view(), name='api_register'),
    
    # path('email-verification/<uidb64>/<token>/', EmailVerificationConfirmAPIView.as_view(), name='email_verification_confirm'),
    # path('email-verification/', EmailVerificationRequestAPIView.as_view(), name='email_verification_request'),

    # path('reset-password/', ResetPasswordRequestAPIView.as_view(), name='reset_password_request'),
    # path('reset-password/<uidb64>/<token>/', ResetPasswordConfirmAPIView.as_view(), name='reset_password_confirm'),

    # path('google_auth/', GoogleAuth.as_view(), name='google_auth'),
    # path('google_auth_callback/', GoogleAuthCallback.as_view(), name='google_auth_callback'),  # add path for google authentication
    
]