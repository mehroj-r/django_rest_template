from django.urls import path

from core.api.views.auth import LoginAPIView, RefreshAPIView, TokenVerifyAPIView

app_name = "auth"

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", RefreshAPIView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyAPIView.as_view(), name="token_verify"),
]
