from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from .utils import validate_alphanumeric_username
from django_sqids import SqidsField

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    sqid = SqidsField(real_field_name="id")
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, validators=[validate_alphanumeric_username],db_index=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Add related_name to avoid clashes
    # Agroups = models.ManyToManyField(
       # A 'auth.Group',
        # Arelated_name='myuser_set',  # Add a unique related_name for the my user model
        # Ablank=True,
    # A)
    # Auser_permissions = models.ManyToManyField(
       # A 'auth.Permission',
        # Arelated_name='myuser_permissions_set',  # Add a unique related_name for the my user model
        # Ablank=True,
    # A)

    def __str__(self):
        return self.email


# Profile model extending Account
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # avatar = models.ImageField(
    #     upload_to='avatars/',
    #     validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    #     blank=True,
    #     null=True
    # )
    bio = models.TextField(max_length=500, blank=True)