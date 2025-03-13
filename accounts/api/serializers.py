from rest_framework import serializers
from ..models import User, Profile
from ..utils import validate_alphanumeric_username
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
from core.serializers import BaseSerializer

class ProfileSerializer(BaseSerializer):
    class Meta:
        model = Profile
        exclude =['user']


class UserSerializer(BaseSerializer):
    # If you want to include the profile data in the user serializer
    profile = ProfileSerializer(read_only=True)

    custom_field = serializers.SerializerMethodField()
    
    def get_custom_field(self, obj):
        # This method will return the value for 'custom_field'
        return "hello"

    class Meta:
        model = User
        exclude =['password']
        # fields = ('sqid', 'email', 'username', 'first_name', 'last_name', 'date_joined', 
        #           'is_active', 'email_verified', 'is_staff', 'profile')  # Customize this list as needed

    # Optionally, if you want to add custom validation or additional behavior
    def validate_email(self, value):
        # Example of custom email validation (you can add your own rules)
        if 'example.com' in value:
            raise serializers.ValidationError("Email domain 'example.com' is not allowed.")
        return value

    def create(self, validated_data):
        """
        Custom create method if you need additional actions when creating the user.
        """
        user = User.objects.create_user(**validated_data)  # Ensure you use `create_user` to handle password hashing
        return user

    def update(self, instance, validated_data):
        """
        Custom update method to handle updating a user instance.
        """
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.email_verified = validated_data.get('email_verified', instance.email_verified)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance


# Simplified UserSerializer for other models
class UserListSerializer(BaseSerializer):
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)  # Accessing avatar from the related Profile model
    
    class Meta:
        model = User  # Assuming User model is the same one used in `created_by` and `updated_by`
        fields = ['username', 'first_name', 'last_name' , 'avatar']  # Include only the fields you need

    # avatar = serializers.SerializerMethodField()
    # def get_avatar(self, obj):
    #     # Assuming User model has a related 'profile' field
    #     return obj.profile.avatar.url if obj.profile and obj.profile.avatar else None

class RegisterSerializer(BaseSerializer):
    username = serializers.CharField(required=True, min_length=3, validators=[validate_alphanumeric_username])
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8, validators=[validate_password] )
    password_confirmation = serializers.CharField(write_only=True, min_length=8,  required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirmation']
    
    def validate(self, data):
        """
        Check that the password and password_confirmation match.
        """
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Şifreler uyuşmuyor.")
        return data

    def validate_email(self, value):
        """
        Check that the email is unique and valid.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Eposta kullanımda.")
        return value

    def validate_username(self, value):
        """
        Check that the username is unique and valid.
        """
        reserved_usernames = ['register', 'token', 'verify']
        if value in reserved_usernames:
            raise serializers.ValidationError(f"Kullanıcı adı kullanımda.")
    
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Kullanıcı adı kullanımda.")
        return value

    def create(self, validated_data):
        """
        Create the user and also create an associated Profile.
        """
        # Remove the re_password as it’s not needed for the user creation
        validated_data.pop('password_confirmation')

        # Create the user
        user = User.objects.create_user(**validated_data)  # This ensures password is hashed
        
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Check if the email exists in the system.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Kayıtlı eposta bulunamadı")
        return value
    

class PasswordResetConfirmSerializer(serializers.Serializer):

    new_password1 = serializers.CharField(
        label="New password confirmation",
        style={'input_type': 'password'},
        trim_whitespace=False,
        required=True
    )
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """
        Check that the password and re_password match.
        """
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({"new_password2": "Şifreler uyuşmuyor."})
        return data
    
    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

# from django.utils.encoding import force_str
# from django.utils.http import  urlsafe_base64_decode

# class UidTokenSerializer(serializers.Serializer):
#     uidb64 = serializers.CharField(required=True, min_length=3)
#     token = serializers.CharField(required=True, min_length=3)

#     def validate_ıidb64(self, value):
#         """
#         Check if the email exists in the system.
#         """

#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)

#         if not User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("Kayıtlı eposta bulunamadı")
#         return value