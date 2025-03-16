from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from ..forms import CustomEmailChangeForm
from ..utils import generate_token_and_uid
from ..emails import verification_email, change_email_email
from core.email_handler import send_email_handler
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from ..models import EmailChangeRequest
from django.contrib.auth.decorators import login_required

def email_verify_view(request):
    try:
        # Decode the uid to get the user ID
        user=request.user
        token, uid = generate_token_and_uid(user)
        # Call email handler (decides between sync or async automatically)
        if not user.email_verified:
            send_email_handler(verification_email, user.username, user.email, token, uid)
            return redirect('core:home')
        else:
            messages.error(request, "Eposta zaten doğrulanmış.")
            return redirect('core:home')

    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request, "Link hatalı veya süresi geçmiş.")
        return redirect('core:home')


def email_verify_confirm_view(request, uidb64, token):
    try:
        # Decode the uid to get the user ID
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(id=uid)

        # Check if the token is valid for the user
        if default_token_generator.check_token(user, token):
            user.email_verified=True
            user.save()
            messages.success(request, 'Epostanız başarıyla doğrulandı.')
            return redirect('core:home')

        else:
            messages.error(request, "Link hatalı veya süresi geçmiş.")
            return redirect('core:home')

    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request, "Link hatalı veya süresi geçmiş.")
        return redirect('core:home')

@login_required
def email_change_view(request):
    if request.method == "POST":
        form = CustomEmailChangeForm(request.POST, user=request.user)
        if form.is_valid():
            new_email = form.cleaned_data["new_email"]
            password = form.cleaned_data["password"]

            # Authenticate user with current password
            user = authenticate(request, username=request.user.username, password=password)
            if not user:
                messages.error(request, "Şifreniz yanlış.")
                return render(request, "accounts/email_change.html", {"form": form})

            # Create a pending email change request
            email_change_request, created = EmailChangeRequest.objects.get_or_create(user=user)
            email_change_request.new_email = new_email
            email_change_request.confirmed = False
            email_change_request.save()

            # Generate UID and token
            token, uid = generate_token_and_uid(user)

            send_email_handler(change_email_email, user.username, new_email, token, uid)

            messages.success(request, "Yeni e-posta adresinizi doğrulamak için size bir bağlantı gönderdik.")
            return redirect('core:home')

    else:
        form = CustomEmailChangeForm()

    return render(request, "accounts/email_change.html", {"form": form})


def email_change_confirm_view(request, uidb64, token):
    try:
        # Decode the uid to get the user ID
        uid = urlsafe_base64_decode(uidb64).decode()
        email_change_request = EmailChangeRequest.objects.get(user=uid)


        # Validate the token
        if default_token_generator.check_token(email_change_request.user, token):
            # Update the user's email address with the new one
            user = email_change_request.user
            user.email = email_change_request.new_email
            user.save()

            # Mark the request as confirmed
            email_change_request.confirmed = True
            email_change_request.save()

            messages.success(request, "Epostanız başarıyla değiştirildi.")
            return redirect('core:home')

        else:
            messages.error(request, "Link hatalı veya süresi geçmiş.")
            return redirect('accounts:login')

    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request, "Link hatalı veya süresi geçmiş.")
        return redirect('core:home')