from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # Enables language switching
]

# API and Rosetta should NOT be affected by i18n
urlpatterns += [
    path("api/", include("lang_manager.urls")),  # API should remain language-neutral
    path("rosetta/", include("rosetta.urls")),  # Rosetta should remain language-neutral
]

# Apply language prefix to Django Admin and lang_manager
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("lang_manager/", include("lang_manager.admin_urls")),  # Ensure admin actions respect i18n
    path("", include("blog.urls")),
)
