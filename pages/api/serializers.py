from rest_framework import serializers
from ..models import Page
from streamblocks.api.serializers import RichTextSerializer, ImageWithTextSerializer , ImageWithText
from core.serializers import BaseSerializer, StreamSerializer

class PageSerializer(BaseSerializer,StreamSerializer):
    class Meta:
        model = Page
        fields = ['sqid', 'title', 'slug', 'content', 'parent',  "stream"]