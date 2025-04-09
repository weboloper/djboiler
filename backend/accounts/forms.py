from django import forms
from django.contrib.auth import get_user_model
from .utils import validate_alphanumeric_username  # Import your utility function
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password

class CustomRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Use your utility function to validate the username
        validate_alphanumeric_username(username)

        # Check if the username already exists
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError("Bu kullanıcı adına sahip bir hesap zaten mevcut.")
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if the email already exists
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Bu e-posta adresine sahip bir hesap zaten mevcut.")
        
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("username", "")  # Default to empty string
        
        # Apply Django's default password validation
        try:
            validate_password(password)  
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        
        # Custom check: Prevent passwords similar to the username
        if username.lower() in password.lower():
            raise forms.ValidationError("Şifreniz kullanıcı adınıza çok benziyor.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        # Check if passwords match
        if password and password_confirmation:
            if password != password_confirmation:
                self.add_error('password_confirmation', 'Şifreler uyuşmuyor.')
        
        return cleaned_data


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email_or_username = self.cleaned_data.get("email")
        
        # Check if the provided value is an email address or a username
        try:
            if '@' in email_or_username:  # If it's an email
                user = get_user_model().objects.get(email=email_or_username)
            else:  # If it's a username
                user = get_user_model().objects.get(username=email_or_username)
            
            # If the user exists, return the user to send the reset email
            return user
        except get_user_model().DoesNotExist:
            raise ValidationError("Böyle bir kullanıcı yok.")


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Mevcut Şifre")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Yeni Şifre")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Yeni Şifre (Tekrar)")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not check_password(old_password, self.user.password):
            raise forms.ValidationError("Mevcut şifreniz yanlış.")
        return old_password

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get("new_password1")
        try:
            validate_password(new_password1, self.user)  # Django's built-in password validators
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return new_password1

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error("new_password2", "Şifreler uyuşmuyor.")

        return cleaned_data
        

class CustomEmailChangeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Şifre")
    new_email = forms.EmailField(label="Yeni E-posta")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not check_password(password, self.user.password):
            raise forms.ValidationError("Şifreniz yanlış.")
        return password

    def clean_new_email(self):
        new_email = self.cleaned_data.get("new_email")
        user_model = get_user_model()
        if user_model.objects.filter(email=new_email).exists():
            raise forms.ValidationError("Bu e-posta adresi zaten kullanılıyor.")
        return new_email