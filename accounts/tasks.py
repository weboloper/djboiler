from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task
def send_email_task(subject, message, recipient_list):
    """Celery task to send an email asynchronously."""
    _send_email(subject, message, recipient_list)  # Calls the internal function

def _send_email(subject, message, recipient_list):
    """Internal function to send email immediately (used in development mode)."""
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    email.content_subtype = 'html'  # Ensure HTML format
    email.send()
