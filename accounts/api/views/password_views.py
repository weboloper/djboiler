from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from ...api.serializers import (
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
)
from django.conf import settings
from django.utils.http import  urlsafe_base64_decode
from ...emails import verification_email, password_reset_email, change_email_email
from django.utils.encoding import force_str
from ...models import User
from ...utils import generate_token_and_uid
from django.contrib.auth.tokens import default_token_generator
from core.email_handler import send_email_handler
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404


class ResetPasswordRequestAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = get_object_or_404(User, email=request.data.get("email"))
        token, uid = generate_token_and_uid(user)
        send_email_handler(password_reset_email, user.username, user.email, token, uid)

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