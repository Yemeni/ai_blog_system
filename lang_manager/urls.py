from django.urls import path
from .views import list_languages, add_language_view, remove_language_view, generate_translations_view
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

app_name = "lang_manager" 


urlpatterns = [
    path("set_language/", set_language, name="set_language"),  # ✅ Language switcher support
]

