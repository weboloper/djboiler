from rest_framework import serializers
from ..models import Post
from core.serializers import BaseSerializer

class PostSerializer(BaseSerializer):
    class Meta:
        model = Post
        fields = "__all__"