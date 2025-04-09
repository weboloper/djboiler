from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Post
from .serializers import PostSerializer

class PostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Adjust as needed

    def get_object(self, lookup_value, lookup_type="sqid"):
        lookup_field = {
            "sqid": "sqid",
            "slug": "slug"
        }.get(lookup_type, "sqid")  # Default to "sqid"

        filter_kwargs = {lookup_field: lookup_value}
        return get_object_or_404(Post, **filter_kwargs)

    def get(self, request, lookup_value, lookup_type="sqid"):
        post = self.get_object(lookup_value, lookup_type)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)  # Assuming author field
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Full update, missing fieleds set to null or default 
    def put(self, request, lookup_value, lookup_type="sqid"):
        post = self.get_object(lookup_value, lookup_type)
        if post.author != request.user:  # Ensure ownership
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, lookup_value, lookup_type="sqid"):
        post = self.get_object(lookup_value, lookup_type)
        if post.author != request.user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, lookup_value, lookup_type="sqid"):
        post = self.get_object(lookup_value, lookup_type)
        if post.author != request.user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        post.delete()  # Implement soft delete if needed
        return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
