"""
URLs mapping for users.
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import (
    CurrentUserAPIView,
    RegisterAPIView,

    EmailVerificationConfirmAPIView,
    EmailVerificationRequestAPIView,

    ResetPasswordRequestAPIView,
    ResetPasswordConfirmAPIView,

    # GoogleAuth,
    # GoogleAuthCallback
)

urlpatterns = [
    # simple jwt defaults
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify' ),

    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('me/', CurrentUserAPIView.as_view(), name='current_user'),

    path('email-verification/<uidb64>/<token>/', EmailVerificationConfirmAPIView.as_view(), name='email_verification_confirm'),
    path('email-verification/', EmailVerificationRequestAPIView.as_view(), name='email_verification_request'),

    
    path('reset-password/', ResetPasswordRequestAPIView.as_view(), name='reset_password_request'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordConfirmAPIView.as_view(), name='reset_password_confirm'),

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