from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Language

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "add_to_rosetta_parler")

    def add_to_rosetta_parler(self, obj):
        """Creates an action button to add a language to Rosetta & Parler dynamically"""
        url = reverse("lang_manager:add_language_to_rosetta_parler", args=[obj.id])

        return format_html(
            '<a class="button" href="{}">{}</a>',
            url,  # Use Django's `reverse()` to dynamically resolve URL
            _("Add to Rosetta & Parler")
        )
    add_to_rosetta_parler.short_description = _("Add to Rosetta & Parler")

    def get_urls(self):
        """Register custom admin URLs for adding a language"""
        urls = super().get_urls()
        return urls  # No longer need to add the custom URL manually
