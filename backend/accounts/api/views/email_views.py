from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from ...api.serializers import (
    EmailChangeRequestSerializer
)
from django.conf import settings
from django.utils.http import  urlsafe_base64_decode
from ...emails import verification_email,  change_email_email
from django.utils.encoding import force_str
from ...models import User, Profile, EmailChangeRequest
from ...utils import generate_token_and_uid
from django.contrib.auth.tokens import default_token_generator
from core.email_handler import send_email_handler
from django.shortcuts import get_object_or_404

class EmailVerificationRequestAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        if user.email_verified:
            return Response({'detail': 'E-posta doğrulanmış durumda.'}, status=status.HTTP_400_BAD_REQUEST)

        token, uid = generate_token_and_uid(user)
        send_email_handler(verification_email, user.username, user.email, token, uid)

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

            send_email_handler(change_email_email, user.username, new_email, token, uid)

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