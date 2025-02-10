from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import Post
from ..ai import AIProvider
import json

@login_required
def post_create(request):
    if request.method == "POST":
        try:
            # Handle AI Generation (JSON request)
            if request.headers.get('Content-Type') == 'application/json':
                data = json.loads(request.body)
                prompt = data.get('prompt')
                ai_provider = data.get('ai_provider')
                generate_only = data.get('generate_only', False)

                if generate_only:
                    ai_generator = AIProvider()
                    content = ai_generator.generate_content(prompt, ai_provider)
                    return JsonResponse({'title': prompt, 'content': content})

            # Handle Traditional Form Submission
            title = request.POST.get('title')
            content = request.POST.get('content')

            if not title or not content:
                return JsonResponse({'error': 'Title and content are required.'}, status=400)

            post = Post(title=title, content=content, author=request.user)
            post.save()

            return redirect('post_list')  # ✅ Redirect after successful save

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return render(request, 'blog/post_form.html')
