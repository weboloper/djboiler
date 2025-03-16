from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from ...api.serializers import (
    UserSerializer,
    RegisterSerializer, 
)
from ...emails import verification_email
from ...utils import generate_token_and_uid
from core.email_handler import send_email_handler

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
                send_email_handler(verification_email, user.username, user.email, token, uid)
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "message": "Kayıt başarılı!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)