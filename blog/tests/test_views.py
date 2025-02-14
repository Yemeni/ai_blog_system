import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post

@pytest.mark.django_db
def test_post_list_view(client):
    response = client.get(reverse("post_list"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_creation(client):
    user = User.objects.create(username="testuser", password="password")
    client.force_login(user)
    
    response = client.post(reverse("post_create"), {
        "title": "New Post",
        "content": "Testing post creation",
        "author": user.id,
    })
    assert response.status_code == 302  # Redirect to post list
    assert Post.objects.count() == 1
