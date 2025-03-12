from rest_framework import serializers
from account.models import User, Profile
from account.utils import validate_alphanumeric_username
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'avatar', 'bio', 'twitter', 'instagram', 'facebook', 'pinterest')


class UserSerializer(serializers.ModelSerializer):
    # If you want to include the profile data in the user serializer
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'date_joined', 
                  'is_active', 'is_verified', 'is_staff', 'profile')  # Customize this list as needed

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
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance


# Simplified UserSerializer for other models
class UserListSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)  # Accessing avatar from the related Profile model
    
    class Meta:
        model = User  # Assuming User model is the same one used in `created_by` and `updated_by`
        fields = ['username', 'first_name', 'last_name' , 'avatar']  # Include only the fields you need

    # avatar = serializers.SerializerMethodField()
    # def get_avatar(self, obj):
    #     # Assuming User model has a related 'profile' field
    #     return obj.profile.avatar.url if obj.profile and obj.profile.avatar else None

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[validate_alphanumeric_username])
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password] )
    re_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 're_password']
    
    def validate(self, data):
        """
        Check that the password and re_password match.
        """
        if data['password'] != data['re_password']:
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
        validated_data.pop('re_password')

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

    password = serializers.CharField(
        label="New password confirmation",
        style={'input_type': 'password'},
        trim_whitespace=False,
    )
    re_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """
        Check that the password and re_password match.
        """
        if data['password'] != data['re_password']:
            raise serializers.ValidationError({"re_password": "Şifreler uyuşmuyor."})
        return data
    
    def validate_password(self, value):
        password_validation.validate_password(value)
        return value