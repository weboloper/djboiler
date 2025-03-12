from django import forms
from account.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    re_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_re_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('re_password')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
