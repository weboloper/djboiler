from django.db import models
from django_sqids import SqidsField
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder


class BaseModel(models.Model):
    """Base model to replace 'id' with 'sqid'."""
    sqid = SqidsField(real_field_name="id")

    class Meta:
        abstract = True  # Prevent Django from treating this as a real model

class StreamModel(models.Model):

    # stream_json = models.JSONField(encoder=DjangoJSONEncoder, default=dict, blank=True, null=True)
    def serialize_block_content(self, block_content):
        """Convert block_content (model instances) to JSON-friendly dictionaries."""
        if isinstance(block_content, list):
            return [self.serialize_block_content(item) for item in block_content]
        elif isinstance(block_content, models.Model):
            data = {
                "id": block_content.id,
                "title": block_content.title,
                "text": block_content.text
            }
            # If the model has an image field, add its URL
            if hasattr(block_content, "image") and block_content.image:
                data["image_url"] = block_content.image.url
            return data
        return block_content  # Return as is if it's already serializable
    
    def get_cached_stream(self):
        """Retrieve stream data from cache or generate and store it if not cached."""
        cache_key = f"page_stream_{self.id}"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return cached_data  # Return cached data

        # Generate stream JSON if not cached
        if self.stream:
            try:
                stream_data = self.stream.as_list()
                for block in stream_data:
                    block["data"]["block_content"] = self.serialize_block_content(
                        block["data"]["block_content"]
                    )
                cache.set(cache_key, stream_data, timeout=24 * 60 * 60)  # Cache for 1 day
                return stream_data
            except Exception as e:
                print(f"Error serializing stream: {e}")
                return None

    def save(self, *args, **kwargs):
        """Invalidate cache when the Page object is saved."""
        super().save(*args, **kwargs)
        cache.delete(f"page_stream_{self.id}")  # Clear cache on update

    class Meta:
        abstract = True  # Prevent Django from treating this as a real model




class StreamJSONModel(models.Model):

    stream_json = models.JSONField(encoder=DjangoJSONEncoder, default=dict, blank=True, null=True)

    def serialize_block_content(self, block_content):
        """Convert block_content (model instances) to JSON-friendly dictionaries."""
        if isinstance(block_content, list):
            return [self.serialize_block_content(item) for item in block_content]
        elif isinstance(block_content, models.Model):
            data = {
                "id": block_content.id,
                "title": block_content.title,
                "text": block_content.text
            }
            # If the model has an image field, add its URL
            if hasattr(block_content, "image") and block_content.image:
                data["image_url"] = block_content.image.url
            return data
        return block_content  # Return as is if it's already serializable
    
    def get_cached_stream(self):
        """Retrieve stream data from cache or generate and store it if not cached."""
        cache_key = f"page_stream_{self.id}"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return cached_data  # Return cached data

        # Generate stream JSON if not cached
        if self.stream:
            try:
                stream_data = self.stream.as_list()
                for block in stream_data:
                    block["data"]["block_content"] = self.serialize_block_content(
                        block["data"]["block_content"]
                    )
                cache.set(cache_key, stream_data, timeout=24 * 60 * 60)  # Cache for 1 day
                return stream_data
            except Exception as e:
                print(f"Error serializing stream: {e}")
                return None

    def save(self, *args, **kwargs):
        """Precompute stream_json before saving."""
        if self.stream:
            try:
                stream_data = self.stream.as_list()
                for block in stream_data:
                    block["data"]["block_content"] = self.serialize_block_content(
                        block["data"]["block_content"]
                    )
                self.stream_json = stream_data
            except Exception as e:
                print(f"Error serializing stream: {e}")
                self.stream_json = None
        super().save(*args, **kwargs)

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



