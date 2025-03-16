from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..models import Page
from .serializers import PageSerializer

class PageAPIView(APIView):
    def get(self, request, slug):
        try:
            # Fetch the page object by slug
            page = Page.objects.get(slug=slug)
        except Page.DoesNotExist:
            # If the page is not found, raise a 404 error
            raise NotFound("Page not found")

        # Serialize the page object and return the response
        serializer = PageSerializer(page)
        return Response(serializer.data)
