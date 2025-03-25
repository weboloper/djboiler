from rest_framework import serializers
from ..models import Page
from core.serializers import BaseSerializer

class PageSerializer(BaseSerializer):
    class Meta:
        model = Page
        fields = ['sqid', 'title', 'slug', 'content', 'parent']