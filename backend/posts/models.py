from django.db import models
from core.models import BaseModel,StreamModel
from streamblocks.models import RichText, ImageWithText
from streamfield.fields import StreamField

# Create your models here.
class Post(BaseModel,StreamModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True, null=True)  # Optional description for the variant type
    stream = StreamField(
        model_list=[ 
            RichText,
            ImageWithText
        ],
        verbose_name="Page blocks"
        )
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    