from django.db import models
from django.contrib.auth.models import User
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _

class Post(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_('title'),max_length=200),
        content = models.TextField(_('content')),
    )

    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
