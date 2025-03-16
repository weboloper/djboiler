from django.shortcuts import render
from django.contrib.auth import get_user_model,update_session_auth_hash
from django.shortcuts import redirect
from django.contrib import messages
from ..forms import  CustomPasswordResetForm, CustomPasswordChangeForm
from ..utils import generate_token_and_uid
from ..emails import  password_reset_email  
from core.email_handler import send_email_handler
# from config.celery import debug_task
from django.utils.http import  urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm 
from django.contrib.auth.decorators import login_required


def password_reset_request_view(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            # Form handling logic
            # form.save(request=request, use_https=request.is_secure())
            user = form.cleaned_data["email"]  # Access the user object
            token, uid = generate_token_and_uid(user)
            send_email_handler(password_reset_email, user.username, user.email, token, uid)

            messages.success(request, "Şifre sıfırlama bağlantısı gönderildi.")
            return redirect('pages:home')
        else:
            messages.error(request, 'Lütfen aşağıdaki hataları düzeltin.')
    else:
        form = CustomPasswordResetForm()
    
    return render(request, 'accounts/password_reset_request.html', {'form': form})


def password_reset_confirm_view(request, uidb64, token):
    try:
        # Decode the uid to get the user ID
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(id=uid)

        # Check if the token is valid for the user
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Şifreniz başarıyla değiştirildi.")
                    return redirect('accounts:login')
            else:
                form = SetPasswordForm(user)
            return render(request, 'accounts/password_reset_confirm.html', {'form': form, 'user': user})
        else:
            messages.error(request, "Link hatalı veya süresi geçmiş.")
            return redirect('accounts:password_reset_request')

    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request, "Link hatalı veya süresi geçmiş.")
        return redirect('accounts:password_reset_request')
        

@login_required
def password_change_view(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data["new_password1"]
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in

            messages.success(request, "Şifreniz başarıyla değiştirildi.")
            return redirect("pages:home")
        else:
            messages.error(request, 'Lütfen aşağıdaki hataları düzeltin.')
    else:
        form = CustomPasswordChangeForm()

    return render(request, "accounts/password_change.html", {"form": form})
        
