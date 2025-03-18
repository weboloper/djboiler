from rest_framework import serializers
from ..models import Page
from streamblocks.api.serializers import RichTextSerializer, ImageWithTextSerializer

class PageSerializer(serializers.ModelSerializer):
    # stream = serializers.SerializerMethodField() 
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'content', 'parent', "stream_json"]

    def get_stream(self, obj):
        stream_data = obj.stream.as_list()
        serialized_stream = []
        
        for block in stream_data:
            block_model = block['data']['block_model']
            block_content = block['data']['block_content']

            if block_model == 'richtext':
                serializer = RichTextSerializer(block_content)
            elif block_model == 'imagewithtext':
                serializer = ImageWithTextSerializer(block_content, many=True)
            else:
                serializer = None

            serialized_stream.append({
                'block_model': block_model,
                'block_unique_id': block['data']['block_unique_id'],
                'block_content': serializer.data if serializer else None,
                'template': block['template'],
            })

        return serialized_stream
