from django.conf import settings
from .tasks import send_email_task  # Import from tasks.py

def send_email_handler(email_function, *args, **kwargs):
    """
    Handles email sending logic based on DEBUG mode.

    - `email_function`: The function that prepares the email (e.g., `prepare_verification_email`).
    - `args`: Arguments to pass to the email function.
    - `kwargs`: Keyword arguments to pass to the email function.
    """
    subject, message, recipient_list = email_function(*args, **kwargs)

    send_email_task.delay(subject, message, recipient_list)  # Run asynchronously
    
    # if settings.DEBUG:
    #     send_email_task(subject, message, recipient_list)  # Run synchronously
    # else:
    #     send_email_task.delay(subject, message, recipient_list)  # Run asynchronously
