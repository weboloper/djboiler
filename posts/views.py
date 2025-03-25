from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def post_detail_view(request, slug):
    # Fetch the post object by slug or raise a 404 error if not found
    post = get_object_or_404(Post, slug=slug)
    
    # Render the post with the 'post_detail.html' template
    return render(request, 'posts/post_detail.html', {'post': post})