from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Page
from core.emails import test_email
from core.email_handler import send_email_handler
from django.contrib import messages

# Create your views here.
def home_view(request):
    if request.method == "POST":
        send_email_handler(test_email)
        messages.error(request, 'Eposta gönderildi')
    return render(request, 'pages/home.html')

# Create your views here.
def page_detail_view(request, slug):
    # Fetch the page object by slug or raise a 404 error if not found
    page = get_object_or_404(Page, slug=slug)
    
    # Render the page with the 'page_detail.html' template
    return render(request, 'pages/page_detail.html', {'page': page})