from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    """Automatically replaces 'id' with 'sqid' in all serializers."""
    
    sqid = serializers.CharField(read_only=True)  # Map `sqid` to `id`

    class Meta:
        abstract = True  # Prevent Django from treating this as a real serializer

    def get_fields(self):
        """Dynamically remove 'id' and replace with 'sqid'."""
        fields = super().get_fields()
        fields.pop("id", None)  # Remove `id` if it exists
        return fields

        
class StreamSerializer(serializers.Serializer):
    """Handles serialization of the `stream` field with caching."""
    stream = serializers.SerializerMethodField()

    def get_stream(self, obj):
        """Retrieve stream from cache or regenerate it if not found."""
        return obj.get_cached_stream()