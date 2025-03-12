from django.shortcuts import render
from django.contrib.auth import authenticate, login , logout, get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CustomRegistrationForm, CustomPasswordResetForm, CustomEmailChangeForm
from .utils import generate_token_and_uid
from .emails import verification_email, test_email , password_reset_email , change_email_email
from core.email_handler import send_email
from config.celery import debug_task
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from .models import EmailChangeRequest
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.decorators import user_passes_test
# def is_admin(user):
#     return user.is_staff  # or user.is_superuser

# @user_passes_test(is_admin)

# from django.contrib.auth.decorators import permission_required

# @permission_required('blog.can_add_post', raise_exception=True)
# def create_post(request):
#     return render(request, "blog/create_post.html")


from django.http import JsonResponse

def csp_report(request):
    return JsonResponse({"status": "CSP violation logged."})

from django.http import HttpResponse

def test_email_view(request):
    send_email(test_email)
    messages.success(request, 'Test email sent.')
    return HttpResponse("Test email sent.")


# In case you want a custom login form handling or logic
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:home')  # Redirect to the home page or dashboard
        else:
            # Show login error
            messages.error(request, 'Hatalı giriş bilgileri')
    return render(request, 'accounts/login.html')


def logout_view(request):
    """
    Logs out the user and redirects to the homepage.
    """
    logout(request)  # End the user session
    return redirect('core:home')  # Redirect to the homepage or any other page

def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Generate token and UID
            token, uid = generate_token_and_uid(user)
            # Call email handler (decides between sync or async automatically)
            if not user.email_verified:
                send_email(verification_email, user.username, user.email, token, uid)
            messages.success(request, 'Hesabınız oluşturuldu. Giriş yapabilirsiniz.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Lütfen aşağıdaki hataları düzeltin.')
    else:
        form = CustomRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})




def password_reset_request_view(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            # Form handling logic
            # form.save(request=request, use_https=request.is_secure())

            user = form.cleaned_data["email"]  # Access the user object
            token, uid = generate_token_and_uid(user)
            send_email(password_reset_email, user.username, user.email, token, uid)

            messages.success(request, "Şifre sıfırlama bağlantısı gönderildi.")
            return redirect('core:home')
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



def email_verify_view(request, uidb64, token):
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

            send_email(change_email_email, user.username, new_email, token, uid)

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

        # Ensure the request is for the current user and is not yet confirmed
        if email_change_request.user == request.user and not email_change_request.confirmed:
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

        else:
            messages.error(request, "Eposta değişikliği talebinde hata var veya zaten değiştirildi")
            return redirect('core:home')

    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request, "Link hatalı veya süresi geçmiş.")
        return redirect('core:home')