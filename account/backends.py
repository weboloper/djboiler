from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db import models  # Import models from Django ORM
from django.conf import settings

class EmailOrUsernameModelBackend(ModelBackend):    
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find user by username or email (case-insensitive)
            user = User.objects.get(
                models.Q(username__iexact=username) | models.Q(email__iexact=username)
            )
        except User.DoesNotExist:
            return None

        # Check the password and if the user can authenticate
        if not user.check_password(password) or not self.user_can_authenticate(user):
            return None
        
        # Check if email verification is required and the user is not verified
        if settings.EMAIL_VERIFICATION_REQUIRED_TO_LOGIN and not user.is_verified:
            return None  # Don't authenticate if email verification is required but user is not verified

        # If everything passes, return the user
        return user