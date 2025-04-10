from django.core.mail import send_mail
from django.conf import settings
import asyncio
from .tasks import send_email_task  # Import from tasks.py

# Async email sending function using asyncio
async def send_email_async(subject, message, recipient_list):
    """Send email asynchronously using asyncio."""
    # This sends the email in a non-blocking way
    await asyncio.to_thread(send_mail, subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

def send_email_handler(email_function, *args, **kwargs):
    """
    Handles email sending logic based on the configured email method in settings.

    - `email_function`: The function that prepares the email (e.g., `prepare_verification_email`).
    - `args`: Arguments to pass to the email function.
    - `kwargs`: Keyword arguments to pass to the email function.
    """
    subject, message, recipient_list = email_function(*args, **kwargs)

    if settings.DEBUG:
        print(f"EMAIL_METHOD", settings.EMAIL_METHOD)
        print(f"EMAIL_BACKEND", settings.EMAIL_BACKEND)

    if settings.EMAIL_METHOD == 'async':
        # If async email method is selected, use asyncio.create_task to run the async function
        asyncio.create_task(send_email_async(subject, message, recipient_list))
    elif settings.EMAIL_METHOD == 'celery' and settings.USE_CELERY:
        # Use Celery for background email sending
        send_email_task.delay(subject, message, recipient_list)
    else:
        # Send email synchronously (default behavior)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
