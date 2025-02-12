from django.contrib import admin
from .models import Post
from parler.admin import TranslatableAdmin


# @admin.register(Post)
# class PostAdmin(TranslatableAdmin):
#     list_display = ("title", "created_at")
admin.site.register(Post, TranslatableAdmin)
