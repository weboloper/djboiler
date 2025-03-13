from django.db import models
from django_sqids import SqidsField

class BaseModel(models.Model):
    """Base model to replace 'id' with 'sqid'."""
    sqid = SqidsField(real_field_name="id")

    class Meta:
        abstract = True  # Prevent Django from treating this as a real model
        
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This makes this model abstract, i.e., it won't be used directly.

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True  # This model won't be used directly.

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = models.functions.Now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()



