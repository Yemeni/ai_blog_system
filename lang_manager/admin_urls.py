from django.urls import path
from .views import add_language_to_rosetta_parler

app_name = "lang_manager"

urlpatterns = [
    path("add_language_to_rosetta_parler/<int:lang_id>/", add_language_to_rosetta_parler, name="add_language_to_rosetta_parler"),
]
