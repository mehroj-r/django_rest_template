from django.urls import path, include

app_name = "url_router"

urlpatterns = [
    path("users/", include("apps.account.urls", namespace="account")),
    path("auth/", include("apps.core.urls.auth_urls", namespace="auth")),
    path("health/", include("apps.core.urls.health_urls", namespace="health")),
]
