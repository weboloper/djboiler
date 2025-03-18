from rest_framework import serializers
from ..models import RichText, ImageWithText

class RichTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = RichText
        fields = ['title', 'text']

class ImageWithTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageWithText
        fields = ['title', 'image', 'text']