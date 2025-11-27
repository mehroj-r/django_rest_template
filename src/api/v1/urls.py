from django.urls import path, include

app_name = "url_router"

urlpatterns = [
    path("users/", include("api.v1.account.urls", namespace="account")),
    path("auth/", include("api.v1.core.urls.auth", namespace="auth")),
    path("misc/", include("api.v1.core.urls.misc", namespace="health")),
]
