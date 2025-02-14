from django.urls import path
from django.views.i18n import set_language

app_name = "lang_manager" 


urlpatterns = [
    path("set_language/", set_language, name="set_language"),  # Language switcher support
]

