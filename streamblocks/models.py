from django.db import models

# Create your models here.
# streamblocks/models.py

# one object
class RichText(models.Model):
    title = models.CharField(max_length=255,blank=True, null=True)
    text = models.TextField(blank=True, null=True)   
    
    def __str__(self):
        # This text will be added to block title name. 
        # For better navigation when block is collapsed.
        return self.text[:30]

    class Meta:
        # This will use as name of block in admin
        # See also STREAMFIELD_BLOCK_TITLE in settings
        verbose_name="Text"

# list of objects
class ImageWithText(models.Model):
    title = models.CharField(max_length=255,blank=True, null=True)
    image = models.ImageField(upload_to="folder/")
    text = models.TextField(null=True, blank=True)
    
    # StreamField option for list of objects
    as_list = True
    
    def __str__(self):
        # This text will be added to block title name.
        # For better navigation when block is collapsed.
        return self.text[:30]

    class Meta:
        verbose_name="Image with text"
        verbose_name_plural="Images with text"

# Register blocks for StreamField as list of models
STREAMBLOCKS_MODELS = [
    RichText,
    ImageWithText
]