from django.shortcuts import render, get_object_or_404, redirect
from ..models import Post
from django.contrib.auth.decorators import login_required

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            return render(request, "blog/post_edit.html", {"post": post, "error": "Title and content cannot be empty."})

        post.title = title
        post.content = content
        post.save()
        return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_edit.html', {'post': post})
