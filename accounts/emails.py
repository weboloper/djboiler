from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task


@shared_task
def send_test_email_task():
    subject = 'Celery ile Redis Test E-Postası'
    to = ['weboloper@gmail.com']

    # E-posta şablonunu render et
    message = render_to_string('accounts/emails/test_email.html', {
        'username': 'Celery Test Kullanıcısı',
    })

    # E-posta oluştur ve gönder
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, to)
    email.content_subtype = 'html'  # HTML içerik tipi
    email.send()

@shared_task
def send_verification_email(username, email, token, uid):
    subject = 'E-Posta Doğrulama'
    to = [email]

    verification_url = f"{settings.FRONTEND_URL}/email-verification-confirm/{uid}/{token}/"
    
    # E-posta şablonunu render et
    message = render_to_string('accounts/emails/email_verification.html', {
        'username':  username,
        'url':  verification_url,
    })

    # E-posta oluştur ve gönder
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, to)
    email.content_subtype = 'html'  # HTML içerik tipi
    email.send()

@shared_task
def send_request_password_email(username, email, token, uid):
    subject = 'Şifre Sıfırlama'
    to = [email]

    reset_url = f"{settings.FRONTEND_URL}/password-reset/{uid}/{token}/"
    
    # E-posta şablonunu render et
    message = render_to_string('accounts/emails/reset_password_email.html', {
        'username':  username,
        'url':  reset_url,
    })

    # E-posta oluştur ve gönder
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, to)
    email.content_subtype = 'html'  # HTML içerik tipi
    email.send()
