from django.shortcuts import redirect
from .utils import check_user_restriction

def user_restricted_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not check_user_restriction(request.user):
            return redirect('home')  # Redirect to a safe page
        return view_func(request, *args, **kwargs)
    return _wrapped_view
