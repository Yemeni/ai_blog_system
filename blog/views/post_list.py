from django.shortcuts import render
from ..models import Post
from django.utils.translation import get_language

def post_list(request):
    """Render the blog post list with language context."""
    posts = Post.objects.all()
    return render(request, "blog/post_list.html", {"posts": posts, "LANGUAGE_CODE": get_language()})