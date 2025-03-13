from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from ..api.serializers import (
    UserSerializer,
    RegisterSerializer, 
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
    EmailChangeRequestSerializer
)
from django.conf import settings
from django.utils.http import  urlsafe_base64_decode
from ..emails import verification_email, password_reset_email, change_email_email
from django.utils.encoding import force_str
from ..models import User, Profile, EmailChangeRequest
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import generate_token_and_uid
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import redirect
import json
import requests
from django.utils.crypto import get_random_string
from io import BytesIO
from PIL import Image
from core.email_handler import send_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from urllib.parse import urlencode

# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

class CurrentUserAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class RegisterAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if not user.email_verified:
                token, uid = generate_token_and_uid(user)
                send_email(verification_email, user.username, user.email, token, uid)
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "message": "Kayıt başarılı!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationRequestAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        if user.email_verified:
            return Response({'detail': 'E-posta doğrulanmış durumda.'}, status=status.HTTP_400_BAD_REQUEST)

        token, uid = generate_token_and_uid(user)
        send_email(verification_email, user.username, user.email, token, uid)

        response_data = {'message': 'E-postanıza gönderildi.'}
        if settings.ENVIRONMENT == 'dev':
            response_data.update({'token': token, 'uid': uid})
        return Response(response_data, status=status.HTTP_200_OK)


class EmailVerificationConfirmAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        if not uidb64 or not token:
            return Response({"detail": "Geçersiz eposta doğrulama bağlantısı."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError):
            return Response({"detail": "Geçersiz bağlantı."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Geçersiz token."}, status=status.HTTP_400_BAD_REQUEST)

        if user.email_verified:
            return Response({"detail": "E-posta zaten doğrulandı."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.email_verified = True
        user.save()
        return Response({"message": "E-posta doğrulama başarılı."}, status=status.HTTP_200_OK)


class ResetPasswordRequestAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = get_object_or_404(User, email=request.data.get("email"))
        token, uid = generate_token_and_uid(user)
        send_email(password_reset_email, user.username, user.email, token, uid)

        response_data = {'message': 'E-postanıza gönderildi.'}
        if settings.ENVIRONMENT == 'dev':
            response_data.update({'token': token, 'uid': uid})
        
        return Response(response_data, status=status.HTTP_200_OK)


class ResetPasswordConfirmAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        if not uidb64 or not token:
            return Response({"detail": "Geçersiz şifre sıfırlama bağlantısı."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError):
            return Response({"detail": "Geçersiz bağlantı."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Token geçersiz veya süresi dolmuş."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password1"])
            user.save()
            return Response({"message": "Şifreniz başarıyla değiştirildi."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data["new_password1"])
            request.user.save()
            update_session_auth_hash(request, request.user)
            return Response({"message": "Şifreniz başarıyla değiştirildi."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailChangeRequestView(APIView):
    def post(self, request):
        serializer = EmailChangeRequestSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = request.user
            new_email = serializer.validated_data["new_email"]

            # Create a pending email change request
            email_change_request, created = EmailChangeRequest.objects.get_or_create(user=user)
            email_change_request.new_email = new_email
            email_change_request.confirmed = False
            email_change_request.save()

            # Generate UID and token
            token, uid = generate_token_and_uid(user)

            send_email(change_email_email, user.username, new_email, token, uid)

            response_data = {'message': 'E-postanıza gönderildi.'}
            if settings.ENVIRONMENT == 'dev':
                response_data.update({'token': token, 'uid': uid})
            
            return Response(response_data, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmailChangeConfirmView(APIView):
     permission_classes = (permissions.AllowAny,)
     def post(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        
        if not uidb64 or not token:
            return Response({"detail": "Geçersiz eposta doğrulama bağlantısı."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError):
            return Response({"detail": "Geçersiz bağlantı."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Token geçersiz veya süresi dolmuş."}, status=status.HTTP_400_BAD_REQUEST)

        email_request = EmailChangeRequest.objects.filter(user=user, confirmed=False).first()
        if not email_request:
            return Response({"error": "Geçersiz istek."}, status=status.HTTP_400_BAD_REQUEST)

        # Update user email
        user.email = email_request.new_email
        user.save()
        email_request.confirmed = True
        email_request.save()

        return Response({"message": "E-posta başarıyla güncellendi."}, status=status.HTTP_200_OK)
    
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