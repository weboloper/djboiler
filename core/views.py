from django.shortcuts import render
from django.http import JsonResponse
from .emails import test_email
from .email_handler import send_email
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def home_view(request):
    return render(request, 'core/home.html')

def csp_report(request):
    return JsonResponse({"status": "CSP violation logged."})

def test_email_view(request):
    send_email(test_email)
    messages.success(request, 'Test email sent.')
    return redirect('core:home')