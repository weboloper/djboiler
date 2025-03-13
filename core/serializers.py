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

        
