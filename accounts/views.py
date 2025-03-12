from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import CustomRegistrationForm
from .utils import generate_token_and_uid
from .emails import send_verification_email

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

def home_view(request):
    return render(request, 'accounts/home.html')

# In case you want a custom login form handling or logic
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')  # Redirect to the home page or dashboard
        else:
            # Show login error
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')


def logout_view(request):
    """
    Logs out the user and redirects to the homepage.
    """
    logout(request)  # End the user session
    return redirect('accounts:home')  # Redirect to the homepage or any other page

def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Generate token and UID
            token, uid = generate_token_and_uid(user)
            send_verification_email.delay(user.username, user.email, token, uid )
            messages.success(request, 'Account created successfully.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})