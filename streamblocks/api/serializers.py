from rest_framework import serializers
from ..models import RichText, ImageWithText
from django.conf import settings

class RichTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = RichText
        fields = ['title', 'text']

class ImageWithTextSerializer(serializers.ModelSerializer):
    # image_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageWithText
        fields = ['title', 'image', 'text']

    def get_image_url(self, obj):
        request = self.context.get('request', None)

        if obj.image:
            image_url = obj.image.url

            print(image_url)

            # If image_url is already a full URL (e.g., AWS S3 or external link), return as is
            if image_url.startswith("http"):
                return image_url  

            # If request exists, return full URL using request
            if request:
                return request.build_absolute_uri(image_url)

            # Fallback to SITE_URL if request is None
            return f"{settings.SITE_URL}/{image_url}"

        return None
