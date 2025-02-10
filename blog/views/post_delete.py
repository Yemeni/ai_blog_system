from django.shortcuts import get_object_or_404, redirect
from ..models import Post
from django.contrib.auth.decorators import login_required

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
