from django.urls import path
from .views import add_language_view, remove_language_view, list_languages  # ✅ Import new JSON-based views

app_name = "lang_manager"

urlpatterns = [
    path("list/", list_languages, name="list_languages"),
    path("add/", add_language_view, name="add_language"),
    path("remove/", remove_language_view, name="remove_language"),
]
