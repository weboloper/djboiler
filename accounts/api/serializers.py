from rest_framework import serializers
from ..models import User, Profile, EmailChangeRequest
from ..utils import validate_alphanumeric_username
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
from core.serializers import BaseSerializer

class ProfileSerializer(BaseSerializer):
    class Meta:
        model = Profile
        exclude =['user']


class UserSerializer(BaseSerializer):
    profile = ProfileSerializer(read_only=True, allow_null=True)

    class Meta:
        model = User
        exclude =['password']

    def validate_email(self, value):
        if 'example.com' in value:
            raise serializers.ValidationError("Email domain 'example.com' is not allowed.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserListSerializer(BaseSerializer):
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name' , 'avatar']  


class RegisterSerializer(BaseSerializer):
    username = serializers.CharField(required=True, min_length=3, validators=[validate_alphanumeric_username])
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8, validators=[validate_password] )
    password_confirmation = serializers.CharField(write_only=True, min_length=8,  required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirmation']
    
    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Şifreler uyuşmuyor.")
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Eposta kullanımda.")
        return value

    def validate_username(self, value):
        reserved_usernames = ['register', 'token', 'verify','admin']
        if value in reserved_usernames or User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Kullanıcı adı kullanımda.")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)  # This ensures password is hashed
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Kayıtlı eposta bulunamadı")
        return value
    

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({"new_password2": "Şifreler uyuşmuyor."})
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Şifreler uyuşmuyor."})
        return value

    def validate(self, data):
        if data["new_password1"] != data["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Şifreler uyuşmuyor."})
        return data

class EmailChangeRequestSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_email = serializers.EmailField()

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['password']):
            raise serializers.ValidationError({"password": "Şifreniz yanlış."})

        if User.objects.filter(email=data['new_email']).exists():
            raise serializers.ValidationError({"new_email": "Eposta kullanımda."})
        
        return data