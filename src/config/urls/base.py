from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.url_router"), name="url_router"),
]

if settings.DEBUG:
    from config.urls import dev

    urlpatterns += dev.urlpatterns
