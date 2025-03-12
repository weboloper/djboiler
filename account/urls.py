from django.urls import path
from .views import *
from django.views.generic import TemplateView

from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    # path('login/', views.login_view, name='login'),
    # path('register/', views.register_view, name='register'),
    # path('logout/', logout_view, name='logout'),
    # path('email-verification-confirm/<uidb64>/<token>/', views.verification_view, name='email_verification'),

    # path('password-reset/', password_reset_request, name='password_reset'),
    # path('password-reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),

    # path('send-email/', send_email_view, name='send_email'),
    # # Add a success URL or view for redirect after email is sent
    # path('email-sent-success/', TemplateView.as_view(template_name='account/email_sent_success.html'), name='email_sent_success'),


    path('api/', include('account.api.urls')),
    # path('auth-receiver', views.auth_receiver, name='auth_receiver'),


    # path('welcome/start', views.welcome_start_view, name='welcome_start'),
    # path('welcome/skin_goals', views.welcome_skin_goals_view, name='welcome_skin_goals'),
    # path('welcome/quiz', views.welcome_quiz_view, name='welcome_quiz'),
    # path('welcome/quiz1', views.welcome_quiz1_view, name='welcome_quiz1'),
    # path('welcome/quiz2', views.welcome_quiz2_view, name='welcome_quiz2'),
    # path('welcome/quiz3', views.welcome_quiz3_view, name='welcome_quiz3'),
    # path('welcome/quiz_result', views.welcome_quiz_result_view, name='welcome_quiz_result'),
    # path('welcome/quiz_known', views.welcome_quiz_known_view, name='welcome_quiz_known'),


]