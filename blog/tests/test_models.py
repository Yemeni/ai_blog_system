import pytest
from blog.models import Post
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_post():
    user = User.objects.create(username="testuser")
    post = Post.objects.create(title="Test Post", content="This is a test post.", author=user)
    
    assert post.title == "Test Post"
    assert post.content == "This is a test post."
    assert post.author.username == "testuser"
