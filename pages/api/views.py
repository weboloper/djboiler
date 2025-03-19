from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..models import Page
from .serializers import PageSerializer
from rest_framework import permissions
from django.shortcuts import get_object_or_404

class PageAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_object(self, lookup_value, lookup_type="sqid"):
        lookup_field = {
            "sqid": "sqid",
            "slug": "slug"
        }.get(lookup_type, "sqid")  # Default to "sqid"

        filter_kwargs = {lookup_field: lookup_value}
        return get_object_or_404(Page, **filter_kwargs)

    def get(self, request, lookup_value, lookup_type="sqid"):
        page = self.get_object(lookup_value, lookup_type)
        serializer = PageSerializer(page,context={'request': request})
        return Response(serializer.data)