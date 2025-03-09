from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

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
    return render(request, 'users/home.html')

# In case you want a custom login form handling or logic
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:home')  # Redirect to the home page or dashboard
        else:
            # Show login error
            messages.error(request, 'Invalid username or password')
    return render(request, 'users/login.html')


def logout_view(request):
    """
    Logs out the user and redirects to the homepage.
    """
    logout(request)  # End the user session
    return redirect('users:home')  # Redirect to the homepage or any other page