"""
URLs mapping for users.
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from account.api.views import (
    CurrentUserAPIView,
    RegisterAPIView,

    EmailVerificationConfirmAPIView,
    EmailVerificationRequestAPIView,

    ResetPasswordRequestAPIView,
    ResetPasswordConfirmAPIView,

    GoogleAuth,
    GoogleAuthCallback
)

urlpatterns = [
    # simple jwt defaults
    path('users/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify' ),

    path('users/register/', RegisterAPIView.as_view(), name='api_register'),
    path('users/me/', CurrentUserAPIView.as_view(), name='current_user'),

    path('users/email-verification/<uidb64>/<token>/', EmailVerificationConfirmAPIView.as_view(), name='email_verification_confirm'),
    path('users/email-verification/', EmailVerificationRequestAPIView.as_view(), name='email_verification_request'),

    
    path('users/reset-password/', ResetPasswordRequestAPIView.as_view(), name='reset_password_request'),
    path('users/reset-password/<uidb64>/<token>/', ResetPasswordConfirmAPIView.as_view(), name='reset_password_confirm'),

    path('users/google_auth/', GoogleAuth.as_view(), name='google_auth'),
    path('users/google_auth_callback/', GoogleAuthCallback.as_view(), name='google_auth_callback'),  # add path for google authentication
    

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