from django.urls import path, include

app_name = "url_router"

urlpatterns = [
    path("users/", include("account.urls", namespace="account")),
    path("auth/", include("core.urls.auth_urls", namespace="auth")),
    path("health/", include("core.urls.health_urls", namespace="health")),
]
