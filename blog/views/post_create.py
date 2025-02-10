from django.shortcuts import render, redirect
from ..models import Post
from django.contrib.auth.decorators import login_required

@login_required
def post_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post(title=title, content=content, author=request.user)
        post.save()
        return redirect('post_list')
    return render(request, 'blog/post_form.html')
