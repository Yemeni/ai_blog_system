from django.shortcuts import render, get_object_or_404, redirect
from ..models import Post
from django.contrib.auth.decorators import login_required

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html', {'post': post})
