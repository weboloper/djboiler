from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from ..api.serializers import (
    UserSerializer,
    RegisterSerializer, 
    PasswordResetConfirmSerializer
)
from django.conf import settings
from django.utils.http import  urlsafe_base64_decode
from ..emails import send_verification_email, send_request_password_email
from django.utils.encoding import force_str
from ..models import User, Profile
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

class CurrentUserAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
    
    def get(self, request,  format=None):
        user = self.get_object()
        serializer = UserSerializer(user,context={"request": request})
        return Response(serializer.data)
    
    # def put(self, request, *args, **kwargs):
    #     user = self.get_object()

    #     serializer = UserSerializer(user, data=request.data , partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegisterAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            if not settings.VERIFIED_ON_REGISTER:
                app_url = settings.FRONTEND_URL
                token, uid= generate_token_and_uid(user)
                if not settings.DEBUG:
                    send_verification_email.delay(app_url, user.username, user.email, token, uid )                    

                data = serializer.data
                data["token"] = token
                data["uid"] = uid
                
            return Response( data , status=status.HTTP_201_CREATED)
        return Response( serializer.errors  , status=status.HTTP_400_BAD_REQUEST)
    

class EmailVerificationConfirmAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        

        if uidb64 is None or token is None :
            return Response({'detail': 'Doğrulama bağlantısı geçersiz. Lütfen tekrar deneyiniz.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError) as e:
            return Response({'detail': 'Invalid token or UID.'}, status=status.HTTP_400_BAD_REQUEST)

        if user is not None and default_token_generator.check_token(user, token):

            if user.is_verified:
                return Response({'detail': 'E-posta doğrulanmış durumda.'}, status=status.HTTP_400_BAD_REQUEST)
            user.is_verified = True
            user.save()
            return Response({'message': 'E-posta doğrulama başarıyla tamamlandı.'}, status=status.HTTP_200_OK)

        else:
            return Response({'detail': 'Doğrulama bağlantısı geçersiz. Lütfen tekrar deneyiniz.'}, status=status.HTTP_400_BAD_REQUEST)
        
class EmailVerificationRequestAPIView(APIView):
    
    permission_classes = (permissions.AllowAny,)
    def post(self, request):

        try:
            user = User.objects.get(email=request.data.get("email"))

            if user.is_verified:
                return Response({'detail': 'E-posta doğrulanmış durumda.'}, status=status.HTTP_400_BAD_REQUEST)
            app_url = settings.FRONTEND_URL
            token, uid = generate_token_and_uid(user)
            if settings.DEBUG:
                return Response({'token': token,  "uid": uid}, status=status.HTTP_200_OK)
            send_verification_email.delay(app_url,user.username, user.email, token, uid )

        except User.DoesNotExist:
            return Response({'detail': 'Böyle bi hesap yok.'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordRequestAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):

        try:
            app_url = settings.FRONTEND_URL
            user = User.objects.get(email=request.data.get("email"))            
            token, uid = generate_token_and_uid(user)
            if settings.DEBUG:
                return Response({'token': token,  "uid": uid}, status=status.HTTP_200_OK)
            send_request_password_email.delay(app_url, user.username, user.email, token, uid )
            return Response({'message': 'Epostanıza gönderildi.'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'detail': 'Böyle bi hesap yok.'}, status=status.HTTP_400_BAD_REQUEST)
        
 


class ResetPasswordConfirmAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        password = request.data.get('password')
        

        if uidb64 is None or token is None or password is None:
            return Response({'detail': 'uidb64, token ve şifre gerekli'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):

            serializer = PasswordResetConfirmSerializer(data=request.data)
            if serializer.is_valid():
                user.set_password(password)
                user.save()
                return Response({'message': 'Şifreniz başarıyla değiştirildi.'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
            
        else:
            return Response({'detail': 'Şifre hatırlatma bağlantısı geçersiz. Lütfen tekrar deneyiniz.'}, status=status.HTTP_400_BAD_REQUEST)




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
        redirect_url = google_oauth_url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
        return redirect(redirect_url)


def unique_username(username):
    counter = 1
    while User.objects.filter(username=username):
        username = username + str(counter)
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
        response = requests.post(token_url, data=data)

        # After getting the response from the token exchange
        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to obtain access token from Google'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = response.json().get('access_token')
        
        # Get user info from Google API
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        if user_info_response.status_code == 200:
            user_info = user_info_response.json()
            username = unique_username(user_info['email'].split('@')[0])
            
            # Get or create user based on Google user info
            user, created = User.objects.get_or_create(email=user_info['email']  )
            if created:
                # If user is created, set additional attributes
                user.username=username
                user.is_active=True
                # user.first_name = user_info.get('given_name', '')
                # user.last_name = user_info.get('family_name', '')
                # user.is_verified = True
                user.save()
            # if not user.is_verified:
            #     user.is_verified = True
            #     user.save()
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
                "refresh": str(refresh)
            }
            
            # Return tokens in JSON response
            return JsonResponse(response_data)
            
        else:
            return JsonResponse({'error':  code}, status=response.status_code)
        
    def random_trailing(self):
        return get_random_string(length=5)