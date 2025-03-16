from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.shortcuts import redirect
import json
import requests
from django.utils.crypto import get_random_string
from io import BytesIO
from PIL import Image
from urllib.parse import urlencode
from ...models import User, Profile

class GoogleAuth(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        app_url = settings.FRONTEND_URL
        # Redirect user to Google OAuth consent screen
        google_oauth_url = "https://accounts.google.com/o/oauth2/auth"
        # redirect_uri = request.build_absolute_uri(reverse('google_auth_callback'))
        redirect_uri= app_url + "/api/google/auth"

        params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'email profile',
        }
        redirect_url = f"{google_oauth_url}?{urlencode(params)}"
        # redirect_url = google_oauth_url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
        return redirect(redirect_url)


def unique_username(username):
    original_username = username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{original_username}{counter}"
        counter += 1
    return username

class GoogleAuthCallback(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        
        app_url = settings.FRONTEND_URL
        json_data = json.loads(request.body)
        code = json_data.get("code")
        if not code:
            return JsonResponse({'error': 'Authorization code not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange authorization code for access token
        # code = request.GET.get('code')
        if not code:
            return JsonResponse({'error': '1Authorization code not found'}, status=status.HTTP_400_BAD_REQUEST)

        token_url = "https://oauth2.googleapis.com/token"
        # redirect_uri = request.build_absolute_uri(reverse('google_auth_callback'))
        redirect_uri= app_url + "/api/google/auth"
        data = {
            'code': code,
            'client_id' : settings.GOOGLE_CLIENT_ID,
            'client_secret' : settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        response = requests.post(token_url, data=data, timeout=5)

        # After getting the response from the token exchange
        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to obtain access token from Google'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = response.json().get('access_token')
        
        # Get user info from Google API
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers, timeout=5)
        if user_info_response.status_code == 200:
            user_info = user_info_response.json()
            username = unique_username(user_info['email'].split('@')[0])
            
            # Get or create user based on Google user info
            user, created = User.objects.get_or_create(email=user_info['email']  )
            if created:
                # If user is created, set additional attributes
                user.username=username
                user.is_active=True
                user.email_verified=True
                # user.first_name = user_info.get('given_name', '')
                # user.last_name = user_info.get('family_name', '')
                user.save()

            # Fetch user's profile image from Google
            profile_image_url = user_info.get('picture')
            if profile_image_url:
                try:
                    response = requests.get(profile_image_url)
                    if response.status_code == 200:
                        # Open image using PIL
                        image = Image.open(BytesIO(response.content))
                        # Resize the image if needed
                        image.thumbnail((300, 300))
                        # Save the image to user's profile model
                        user_profile, created = Profile.objects.get_or_create(user=user)
                        
                        # Convert image to bytes
                        img_byte_array = BytesIO()
                        image.save(img_byte_array, format='JPEG')
                        img_byte_array.seek(0)
                        
                        user_profile.avatar.save(f'{user.username}_avatar.jpg', img_byte_array, save=True)
                except requests.RequestException as e:
                    print(e)
                    # logger.error(f"Failed to download profile image: {e}")
            else:
                # Optionally, set a default profile image
                user_profile.avatar = 'default_avatar.jpg'  # Assuming a default image path exists
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            
            # Prepare response JSON
            response_data = {
                "access": access,
                "refresh": str(refresh),
                "username": user.username,
                "email": user.email,
            }
            
            # Return tokens in JSON response
            return JsonResponse(response_data)
            
        else:
            return JsonResponse({'error':  code}, status=response.status_code)
        
    def random_trailing(self):
        return get_random_string(length=5)