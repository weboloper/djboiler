from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import re
from django_sqids import SqidsField

def validate_username(value):
    if not re.match(r'^[a-zA-Z0-9]+$', value):
        raise ValidationError(
            'Kullanıcı adı sadece alfanümerik karakterlerden oluşabilir',
            code='invalid_username'
        )

# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not username:
            raise ValueError(_('The Username field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)

# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    sqid = SqidsField(real_field_name="id")
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, unique=True, validators=[validate_username],db_index=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_verified = models.BooleanField(_('email verified'), default=settings.VERIFIED_ON_REGISTER)
    is_staff = models.BooleanField(_('staff status'), default=False)

    #moderation
    deleted_at = models.DateTimeField(_('deleted at'), blank=True, null=True)
    deleted_by = models.ForeignKey('self', null=True, blank=True, related_name='deleted_users', on_delete=models.SET_NULL)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# Profile model extending Account
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(
        upload_to='avatars/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True
    )
    bio = models.TextField(_('bio'), max_length=500, blank=True)


    # # Skin Preferences
    # SKIN_TYPE_CHOICES = [
    #     ('dry', 'Kuru'),
    #     ('normal', 'Normal'),
    #     ('oily', 'Yağlı'),
    # ]
    # skin_type = models.CharField(max_length=10, choices=SKIN_TYPE_CHOICES, default="normal")
    # skin_concerns = models.ManyToManyField(SkinConcern, blank=True)

    # # Product Preferences
    # product_preferences = models.ManyToManyField(ProductPreference, blank=True)
    # apply_preferences = models.BooleanField(default=False)
    # hide_avoid_preferences = models.BooleanField(default=False)

    # Social Media Preferences
    twitter = models.CharField(_('Twitter'), max_length=50, blank=True)
    instagram = models.CharField(_('Instagram'), max_length=50, blank=True)
    facebook = models.CharField(_('Facebook'), max_length=50, blank=True)
    pinterest = models.CharField(_('Pinterest'), max_length=50, blank=True)


    def __str__(self):
        return f'{self.user.email} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # If the user was created
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # Save the associated profile if it already exists