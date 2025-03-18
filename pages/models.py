from django.db import models
from core.models import BaseModel
from streamfield.fields import StreamField
from streamblocks.models import RichText, ImageWithText
from streamblocks.api.serializers import RichTextSerializer, ImageWithTextSerializer
from django.core.serializers.json import DjangoJSONEncoder

# Create your models here.
class Page(BaseModel):
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
    stream_json = models.JSONField(encoder=DjangoJSONEncoder, default=dict, blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
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

    def __str__(self):
        return self.title
    
    # # New JSONField for caching stream data
    # def get_stream(self):
    #     """Convert stream data to JSON format."""
    #     stream_data = self.stream.as_list()
    #     serialized_stream = []

    #     for block in stream_data:
    #         block_model = block['data']['block_model']
    #         block_content = block['data']['block_content']

    #         if block_model == 'richtext':
    #             serializer = RichTextSerializer(block_content)
    #         elif block_model == 'imagewithtext':
    #             serializer = ImageWithTextSerializer(block_content, many=True)
    #         else:
    #             serializer = None

    #         serialized_stream.append({
    #             'block_model': block_model,
    #             'block_unique_id': block['data']['block_unique_id'],
    #             'block_content': serializer.data if serializer else None,
    #             'template': block['template'],
    #         })

    #     return serialized_stream
    
    # def save(self, *args, **kwargs):
    #     """Update stream_json before saving."""
    #     self.stream_json = self.get_stream()  # Store precomputed stream data
    #     super().save(*args, **kwargs)

    