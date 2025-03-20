from django.db import models
from core.models import BaseModel

# Create your models here.
class Post(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True, null=True)  # Optional description for the variant type

    def __str__(self):
        return self.title