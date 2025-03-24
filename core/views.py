import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from rest_framework import status
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render

class CustomStorage(FileSystemStorage):
    """Custom storage for django_ckeditor_5 images."""
    def __init__(self,
                 location=settings.MEDIA_ROOT,
                 base_url=settings.MEDIA_URL
                 ):
        super().__init__(location, base_url)

    location = os.path.join(settings.MEDIA_ROOT, "")
    base_url = settings.MEDIA_URL

@csrf_exempt  # Allows requests without CSRF token
def custom_upload_function(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']

        # Generate a unique file name
        filename = get_random_string(length=32) + \
            os.path.splitext(upload.name)[1]
        # Path relative to MEDIA_ROOT
        file_path = os.path.join('', filename)
        # Use custom storage to save the file
        custom_storage = CustomStorage()
        saved_path = custom_storage.save(file_path, ContentFile(upload.read()))

        # Construct the URL for the uploaded file
        file_url = custom_storage.url(saved_path)

        # Return the URL and success response
        return JsonResponse({
            'url': file_url,
            'uploaded': True,
            'status': status.HTTP_201_CREATED
        })

    return JsonResponse({'uploaded': False},
                        status=status.HTTP_400_BAD_REQUEST)


def custom_page_not_found_view(request, exception):
    return render(request, "core/errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "core/errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "core/errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "core/errors/400.html", {})