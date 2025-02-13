from django.shortcuts import redirect
from django.utils.translation import get_language
from django.contrib import messages
from django.conf import settings
from rest_framework import viewsets
from .models import Language
from .serializers import LanguageSerializer

class LanguageViewSet(viewsets.ModelViewSet): 
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

def add_language_to_rosetta_parler(request, lang_id):
    """Handles dynamically adding a language to Django settings & Rosetta"""
    language = Language.objects.get(id=lang_id)
    lang_code = language.code

    # Add the language dynamically to LANGUAGES (Temporary, does not persist)
    if lang_code not in [lang[0] for lang in settings.LANGUAGES]:
        settings.LANGUAGES += ((lang_code, language.name),)

    # Get current language to redirect correctly
    current_lang = get_language()
    admin_url = f"/{current_lang}/admin/lang_manager/language/"

    messages.success(request, f"Language {language.name} ({lang_code}) added successfully!")
    return redirect(admin_url)
