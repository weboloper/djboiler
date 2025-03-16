from django.shortcuts import render
from django.http import JsonResponse
from .emails import test_email
from .email_handler import send_email_handler
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
def home_view(request):
    return render(request, 'core/home.html')

def csp_report(request):
    return JsonResponse({"status": "CSP violation logged."})

def test_email_view(request):
    send_email_handler(test_email)
    return HttpResponse("ok")

# from .tasks import call_task_directly
# def call_task_directly_view(request):
#     call_task_directly.delay()
#     return HttpResponse("ok")
