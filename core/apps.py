from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

from django_summernote.apps import DjangoSummernoteConfig

class CustomDjangoSummernoteConfig(DjangoSummernoteConfig):
    verbose_name = 'MEDIA MANAGER'  # Change this to your desired name