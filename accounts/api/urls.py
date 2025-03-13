"""
URLs mapping for users.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from . import views

app_name = 'api'

urlpatterns = [
    # simple jwt defaults
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify' ),

    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('me/', views.CurrentUserAPIView.as_view(), name='current_user'),

    # password urls
    path('password-reset/', views.ResetPasswordRequestAPIView.as_view(), name='password_reset_request'),
    path('password-reset/<uidb64>/<token>/', views.ResetPasswordConfirmAPIView.as_view(), name='password_reset_confirm'),

    path('email-verify/', views.EmailVerificationRequestAPIView.as_view(), name='email_verify_request'),
    path('email-verify/<uidb64>/<token>/', views.EmailVerificationConfirmAPIView.as_view(), name='email_verify_confirm'),

    # path('google_auth/', GoogleAuth.as_view(), name='google_auth'),
    # path('google_auth_callback/', GoogleAuthCallback.as_view(), name='google_auth_callback'),  # add path for google authentication
    

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