from django.core.exceptions import ValidationError
from account.models import User
import re
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def validate_alphanumeric_username(value):
    if not re.match(r'^[a-zA-Z0-9]+$', value):
        raise ValidationError(
            'Kullanıcı adı sadece alfanümerik karakterlerden oluşabilir',
            code='invalid_username'
        )
    
def unique_username(username):
    counter = 1
    while User.objects.filter(username=username):
        username = username + str(counter)
        counter += 1
        
    return username

def generate_token_and_uid(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return token, uid