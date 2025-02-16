from django.urls import path
from .views import restart_django

urlpatterns = [
    path("restart/", restart_django, name="restart_django"),
]
