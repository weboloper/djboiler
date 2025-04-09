from django.db import models
from core.models import BaseModel 

# Create your models here.
class Page(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True, null=True)  # Optional description for the variant type
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.get_full_path()
    
    def get_full_path(self):
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.slug}"
        return self.slug