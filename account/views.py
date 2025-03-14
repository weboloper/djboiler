from django.shortcuts import render, redirect
from .emails import send_test_email_task
from .forms import UserRegistrationForm
from django.contrib.auth.hashers import make_password
from account.models import User
from .emails import send_request_password_email
from .utils import unique_username
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from .emails import send_verification_email, send_request_password_email


def send_email_view(request):
    if request.method == 'POST':
        send_test_email_task.delay()
        return redirect('account:email_sent_success')
    
    return render(request, 'account/send_email.html')

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        # Attempt to authenticate with either email or username
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            if user.is_active:
                if settings.EMAIL_VERIFICATION_REQUIRED_TO_LOGIN  and not user.is_verified:
                    # Show a warning message that the user needs to verify their email
                    # send_activation_email(user)  # Resend the verification email
                    messages.warning(request, 'Giriş yapabilmek içi e-posta adresinizi doğrulamanız gerekmektedir.')
                    return redirect('account:login')
                
                # If the user is active, log them in
                login(request, user)
                # messages.success(request, 'You have successfully logged in.')
                return redirect('home')  # Redirect to home page after successful login
            else:
                # If the user is inactive, resend the activation email
                messages.error(request, 'Verilen bilgilere ait hesap bulunamadı.')
                return redirect('account:login')  # Redirect back to the login page
            
        else:
            messages.error(request, 'Hatalı giriş bilgileri.')
            return redirect('account:login')  # Redirect back to the login page

    return render(request, 'account/login.html')

def logout_view(request):
    """
    Logs out the user and redirects to the homepage.
    """
    logout(request)  # End the user session
    return redirect('home')  # Redirect to the homepage or any other page

def register_view(request):
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            # Get the correct authentication backend (using your custom backend)
            backend = 'account.backends.EmailOrUsernameModelBackend'
            # Set the backend attribute on the user manually
            user.backend = backend

            if not settings.EMAIL_IS_VERIFIED_ON_REGISTER:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                app_url=settings.APP_URL
                # send_verification_email.delay(app_url,user.username, user.email, token, uid )
                if settings.EMAIL_VERIFICATION_REQUIRED_TO_LOGIN:
                    messages.success(request, 'Hesabınızı doğrulamak için lütfen e-postanızı kontrol ediniz!')
                    return redirect('account:login')
                else:
                    messages.success(request, 'Hesabınızı doğrulamak için e-posta gönderildi. Giriş yapabilirsiniz!')
                    login(request, user, backend=backend)       
                    return redirect('account:welcome_start')
            login(request, user, backend=backend)       
            return redirect('account:welcome_start')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'account/register.html', {'form': form})

def verification_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified=True
        user.save()
        messages.success(request, 'Hesabınız başarıyla doğrulandı. Giriş yapabilirsiniz!')
        return redirect('account:login')
        
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        email = request.POST.get('email', '').strip()  # Get email from POST data and strip whitespace
        if not email:
            # Handle the case where email is empty
            form.add_error(None, 'Lütfen geçerli bir e-posta adresi giriniz!.')
        elif form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            app_url = settings.APP_URL
            if associated_users.exists():
                for user in associated_users:
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    messages.success(request, "Şifre sıfılama bağlantısı e-posta adresinize gönderildi!")
                    # messages.success(request,  f"{app_url}/password-reset/{uid}/{token}/")
                    send_request_password_email.delay(app_url, user.username, user.email, token, uid )
                return redirect('account:login')
            else:
                messages.error(request, 'Böyle bir eposta bulunamadı.')
        else:
            messages.error(request, 'Böyle bir eposta bulunamadı.')
            return render(request, 'account/password_reset_request.html', {'form': form})
            
    else:
        form = PasswordResetForm()
    return render(request, 'account/password_reset_request.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()

                #if user is not verified, email is verified by this action
                if not user.is_verified:
                    user.is_verified=True
                    user.save()

                messages.success(request, 'Şifreniz başarıyla değiştirildi. Giriş yapabilirsiniz.')
                return redirect('account:login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'account/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Şifre değiştirme bağlantısı hatalı veya süresi geçti.')
        return redirect('account:login')
    

@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print('Inside')
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except ValueError:
        return HttpResponse(status=403)

    # Extract email and other user info
    email = user_data.get('email')
    first_name = user_data.get('given_name')
    last_name = user_data.get('family_name')
    
    # Check if the user already exists in your system
    try:
        user = User.objects.get(email=email)
        user.is_verified=True
        user.save()
    except User.DoesNotExist:
        
        username = unique_username(email.split('@')[0])
        # If the user doesn't exist, create a new user
        user = User.objects.create_user(
            email=email,
            username=username,  # You can modify this if needed
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_verified=True
        )
        user.save()

     # Get the correct authentication backend (using your custom backend)
    backend = 'account.backends.EmailOrUsernameModelBackend'
    
    # Set the backend attribute on the user manually
    user.backend = backend
    
    # Authenticate the user and log them in
    login(request, user, backend=backend)

    return redirect('home')  # Redirect to the appropriate page after login



def welcome_start_view(request):
    return render(request, 'account/welcome/start.html')

def welcome_skin_goals_view(request):
    return render(request, 'account/welcome/skin_goals.html')

def welcome_quiz_view(request):
    return render(request, 'account/welcome/quiz.html')

def welcome_quiz1_view(request):
    return render(request, 'account/welcome/quiz1.html')

def welcome_quiz2_view(request):
    return render(request, 'account/welcome/quiz2.html')

def welcome_quiz3_view(request):
    return render(request, 'account/welcome/quiz3.html')

def welcome_quiz_result_view(request):
    return render(request, 'account/welcome/quiz_result.html')

def welcome_quiz_known_view(request):
    return render(request, 'account/welcome/quiz_known.html')

