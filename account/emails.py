from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from django.conf import settings

@shared_task
def send_test_email_task():
    subject = 'Celery with Redis Test Email'
    to = ['weboloper@gmail.com']
    from_email = settings.DEFAULT_FROM_EMAIL

    # Render the email template
    message = render_to_string('accounts/emails/test_email.html', {
        'username': 'Celery Test User',
    })

    # Create and send the email
    email = EmailMessage(subject, message, from_email, to)
    email.content_subtype = 'html'  # Use HTML content type for the email
    email.send()

@shared_task
def send_verification_email(app_url, username, email, token, uid):
    subject = 'Email Verification'
    to = [email]
    from_email = settings.DEFAULT_FROM_EMAIL

    verification_url = f"{app_url}/email-verification-confirm/{uid}/{token}/"
    
    # Render the email template
    message = render_to_string('accounts/emails/email_verification.html', {
        'username':  username,
        'url':  verification_url,
    })

    # Create and send the email
    email = EmailMessage(subject, message, from_email, to)
    email.content_subtype = 'html'  # Use HTML content type for the email
    email.send()

@shared_task
def send_request_password_email(app_url, username, email, token, uid):
    subject = 'Reset Password'
    to = [email]
    from_email = settings.DEFAULT_FROM_EMAIL

    reset_url = f"{app_url}/password-reset/{uid}/{token}/"
    
    # Render the email template
    message = render_to_string('accounts/emails/reset_password_email.html', {
        'username':  username,
        'url':  reset_url,
    })

    # Create and send the email
    email = EmailMessage(subject, message, from_email, to)
    email.content_subtype = 'html'  # Use HTML content type for the email
    email.send()