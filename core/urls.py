from django.urls import path, re_path

from .swagger import schema_view
from .views import restart_django

urlpatterns = [
    path("restart/", restart_django, name="restart_django"),
]

# here are the swagger stuff and the api doc stuff
urlpatterns += [
    # Swagger UI
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),

    # Redoc UI
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # Raw JSON/OpenAPI Schema
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]
