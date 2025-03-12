from django import forms
from django.contrib.auth import get_user_model
from .utils import validate_alphanumeric_username  # Import your utility function
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import check_password


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