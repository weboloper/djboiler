from django.shortcuts import render, get_object_or_404
from .models import Page
from core.emails import test_email
from core.email_handler import send_email_handler
from django.contrib import messages

# Create your views here.
async def home_view(request):
    if request.method == "POST":
        send_email_handler(test_email)
        messages.error(request, 'Eposta gönderildi')
    return render(request, 'pages/home.html')

# Create your views here.
def page_detail_view(request, slug_path):

    slug_parts = slug_path.strip('/').split('/')
    # Start with no parent and find the deepest matching child
    parent = None
    page = None

    for slug in slug_parts:
        page = get_object_or_404(Page, slug=slug, parent=parent)
        parent = page  # Move to the next depth level
    
    # Render the page with the 'page_detail.html' template
    return render(request, 'pages/page_detail.html', {'page': page})