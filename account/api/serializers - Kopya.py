from rest_framework import serializers
from account.models import Profile
from django.contrib.auth.password_validation import validate_password
from account.utils import validate_username
from account.models import User

class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Profile
        fields = [  'bio', 'avatar']
        read_only_fields = ['id', 'user']  # These fields will be read-only


class UserProfileSerializer(serializers.ModelSerializer):
    # pass_set = serializers.SerializerMethodField('has_usable_password')
    # profile = ProfileSerializer(required=True)

    avatar = serializers.ImageField(source='profile.avatar', required=False)
    bio = serializers.CharField(source='profile.bio', required=False)

    # def get_role(self,obj):
    #     role_array = []
    #     if obj.is_superuser:
    #         role_array.append("admin")
    #     if obj.is_staff:
    #         role_array.append("staff")
    #     return role_array
    
    # def has_usable_password(self, obj):
    #     if obj.password == "":
    #         return False
    #     return obj.has_usable_password()
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        avatar = profile_data.get('avatar')
        bio = profile_data.get('bio')
        user = super().update(instance, validated_data)

        # Update profile fields if present
        profile = user.profile
        if avatar:
            profile.avatar = avatar
        if bio:
            profile.bio = bio
        profile.save()

        # # Update the profile fields
        # if profile_data:
        #     Profile.objects.update_or_create(user=user, defaults=profile_data)
        #  # Ensure the profile is correctly reflected in the serialized response
        # instance.profile.refresh_from_db()
        return user

    class Meta:
        model = User
        fields = ("id", 'username', 'email',  "profile" , "is_staff" , "is_verified", "avatar", "bio")
        # read_only_fields = ['pass_set']  # These fields will be read-only

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[validate_username])
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 're_password', 'email')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Kullanıcı adı kullanımda")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu e-posta adresi kullanımda")
        return value

    def validate(self, data):
        if data['password'] != data['re_password']:
            raise serializers.ValidationError({"password": "Şifreler uyuşmuyor"})
        return data

    def create(self, validated_data):
        validated_data.pop('re_password')
        user = User.objects.create_user(**validated_data)
        return user
    
from django.contrib.auth import password_validation
class PasswordResetConfirmSerializer(serializers.Serializer):

    password = serializers.CharField(
        label="New password confirmation",
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value