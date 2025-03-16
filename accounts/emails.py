from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse_lazy

def verification_email(username, email, token, uidb64):
    """
    Prepares the email subject, message, and recipient list for account verification.
    """
    subject = 'E-Posta Doğrulama'
    recipient_list = [email]

    url = reverse_lazy('accounts:email_verify_confirm', kwargs={'uidb64': uidb64 , 'token': token })

    verification_url = f"{settings.FRONTEND_URL + url}"
    
    message = render_to_string('accounts/emails/email_verification.html', {
        'username': username,
        'url': verification_url,
    })

    return subject, message, recipient_list

def password_reset_email(username, email, token, uidb64):
    subject = 'Şifre Sıfırlama'
    recipient_list = [email]

    reset_url = f"{settings.FRONTEND_URL}/password-reset/{uidb64}/{token}/"

    url = reverse_lazy('accounts:password_reset_confirm', kwargs={'uidb64': uidb64 , 'token': token })

    reset_url = f"{settings.FRONTEND_URL + url}"
    
    # E-posta şablonunu render et
    message = render_to_string('accounts/emails/reset_password_email.html', {
        'username':  username,
        'url':  reset_url,
    })
    return subject, message, recipient_list


def change_email_email(username, email, token, uidb64):
    """
    Prepares the email subject, message, and recipient list for account verification.
    """
    subject = 'E-Posta Değişikliği'
    recipient_list = [email]

    url = reverse_lazy('accounts:email_change_confirm', kwargs={'uidb64': uidb64 , 'token': token })

    confirmation_url = f"{settings.FRONTEND_URL + url}"
    
    message = render_to_string('accounts/emails/email_change.html', {
        'username': username,
        'url': confirmation_url,
    })

    return subject, message, recipient_list

# def send_request_password_email(username, email, token, uidb64):
#     subject = 'Şifre Sıfırlama'
#     to = [email]

#     reset_url = f"{settings.FRONTEND_URL}/password-reset/{uidb64}/{token}/"
    
#     # E-posta şablonunu render et
#     message = render_to_string('accounts/emails/reset_password_email.html', {
#         'username':  username,
#         'url':  reset_url,
#     })

#     # E-posta oluştur ve gönder
#     email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, to)
#     email.content_subtype = 'html'  # HTML içerik tipi
#     email.send()
