from rest_framework import serializers
from ..models import Post
from core.serializers import BaseSerializer,StreamSerializer

class PostSerializer(BaseSerializer,StreamSerializer):
    class Meta:
        model = Post
        fields = "__all__"