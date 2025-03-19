from rest_framework import serializers
from ..models import Page
from streamblocks.api.serializers import RichTextSerializer, ImageWithTextSerializer , ImageWithText
from core.serializers import BaseSerializer

class PageSerializer(BaseSerializer):
    # stream = serializers.SerializerMethodField() 
    class Meta:
        model = Page
        fields = ['sqid', 'title', 'slug', 'content', 'parent',  "stream_json"]

    def get_stream(self, obj):
        """
        Convert `stream` into a JSON representation just like `stream_json`.
        """
        if obj.stream:
            try:
                stream_data = obj.stream.as_list()
                for block in stream_data:
                    block["data"]["block_content"] = obj.serialize_block_content(
                        block["data"]["block_content"]
                    )
                return stream_data
            except Exception as e:
                print(f"Error serializing stream: {e}")
                return None
        return None

    def get_stream__(self, obj):
        """
        Convert `stream` into JSON representation just like `stream_json`.
        """
        if obj.stream:
            try:
                stream_data = obj.stream.as_list()
                for block in stream_data:
                    block_content = block["data"]["block_content"]
                   
                    # Check if block_content is a list of ImageWithText instances
                    if isinstance(block_content, list) and all(isinstance(item, ImageWithText) for item in block_content):
                        serializer = ImageWithTextSerializer(block_content, many=True, context=self.context)
                        block["data"]["block_content"] = serializer.data
                    elif isinstance(block_content, ImageWithText):  # Single instance
                        serializer = ImageWithTextSerializer(block_content, context=self.context)
                        block["data"]["block_content"] = serializer.data
                    else:
                        block["data"]["block_content"] = obj.serialize_block_content(block_content)

                return stream_data
            except Exception as e:
                print(f"Error serializing stream: {e}")
                return None
        return None