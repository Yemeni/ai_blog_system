from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LanguageViewSet

router = DefaultRouter()
router.register(r'languages', LanguageViewSet, basename='language')

urlpatterns = [
    path("", include(router.urls)),  # API routes
]
