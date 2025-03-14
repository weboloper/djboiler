from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from ..forms import CustomRegistrationForm
from ..utils import generate_token_and_uid
from ..emails import verification_email
from core.email_handler import send_email
from django.urls import reverse_lazy

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
    auth_receiver_url = reverse_lazy('accounts:auth_receiver')
    context = {
        "auth_receiver_url": auth_receiver_url,
    }
    return render(request, 'accounts/login.html', context )


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