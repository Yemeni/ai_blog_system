from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="AI Blog System API",
        default_version="v1",
        description="API documentation for AI Blog System",
        terms_of_service="https://yourwebsite.com/terms/",
        contact=openapi.Contact(email="your.email@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
