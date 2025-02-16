from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # Enables language switching
]

# API and Rosetta should NOT be affected by i18n
urlpatterns += [
    path("lang_manager/", include("lang_manager.urls")),  
    path("lang_manager/", include("lang_manager.admin_urls")),  
    path("rosetta/", include("rosetta.urls")),  
    path("core/", include("core.urls")), 
]

# Apply language prefix to Django Admin and lang_manager
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
)
