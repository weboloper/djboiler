from django import forms
from django.contrib.auth import get_user_model

class CustomRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalnum():
            raise forms.ValidationError("Username must be alphanumeric.")
        return username
