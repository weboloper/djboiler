from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect
from google.oauth2 import id_token
from google.auth.transport import requests
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse_lazy

def unique_username(username):
    counter = 1
    while get_user_model().objects.filter(username=username):
        username = username + str(counter)
        counter += 1
        
    return username
    
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
        user = get_user_model().objects.get(email=email)
        user.email_verified=True
        user.save()
    except get_user_model().DoesNotExist:
        
        username = unique_username(email.split('@')[0])
        # If the user doesn't exist, create a new user
        user = get_user_model().objects.create_user(
            email=email,
            username=username,  # You can modify this if needed
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            email_verified=True
        )
        user.save()

     # Get the correct authentication backend (using your custom backend)
    # backend = 'account.backends.EmailOrUsernameModelBackend'
    
    # # Set the backend attribute on the user manually
    # user.backend = backend
    
    # Authenticate the user and log them in
    login(request, user)
    # login(request, user, backend=backend)

    return redirect('core:home')  # Redirect to the appropriate page after login