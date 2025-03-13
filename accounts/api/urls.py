"""
URLs mapping for users.
"""
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from . import views

app_name = 'api'

urlpatterns = [
    # simple jwt defaults
    path("token/", include([
        path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('verify/', TokenVerifyView.as_view(), name='token_verify' ),

    ])),

    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('me/', views.CurrentUserAPIView.as_view(), name='current_user'),

    # password urls
    path("password/", include([
        path('reset/', views.ResetPasswordRequestAPIView.as_view(), name='password_reset_request'),
        path('reset/<uidb64>/<token>/', views.ResetPasswordConfirmAPIView.as_view(), name='password_reset_confirm'),
        path('change/', views.ChangePasswordAPIView.as_view(), name='password_change'),

    ])),

    # email urls
    path("email/", include([
        path('verify/', views.EmailVerificationRequestAPIView.as_view(), name='email_verify_request'),
        path('verify/<uidb64>/<token>/', views.EmailVerificationConfirmAPIView.as_view(), name='email_verify_confirm'),
        path('change/', views.EmailChangeRequestView.as_view(), name='email_change_request'),
        path('change/<uidb64>/<token>/', views.EmailChangeConfirmView.as_view(), name='email_change_confirm'),
    ]))

   

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