from django.urls import path
from .views import add_language_view, remove_language_view, list_languages , generate_translations_view, generate_translation_for_language
from .views import list_translations_view, update_translation_view, batch_update_rosetta_translations
app_name = "lang_manager"

urlpatterns = [
    path("list/", list_languages, name="list_languages"),
    path("add/", add_language_view, name="add_language"),
    path("remove/", remove_language_view, name="remove_language"),
    path("generate/", generate_translations_view, name="generate_translations"),
    path("generate/<str:lang_code>/", generate_translation_for_language, name="generate_translation_for_language"),
    path("list_translations/", list_translations_view, name="list_translations"),  
    path("update_translation/", update_translation_view, name="update_translation"),  
    
    path("batch_update_rosetta/", batch_update_rosetta_translations, name="batch_update_rosetta"),


]
