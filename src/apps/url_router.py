from django.urls import path, include

app_name = "url_router"

urlpatterns = [
    path("users/", include("apps.account.urls", namespace="account")),
    path("auth/", include("apps.core.auth_urls", namespace="auth")),
]
